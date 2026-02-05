#!/bin/bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Protected branches that should not be deleted
PROTECTED_BRANCHES=("main" "develop" "master" "staging" "production")

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to check if a branch is protected
is_protected() {
    local branch="$1"
    for protected in "${PROTECTED_BRANCHES[@]}"; do
        if [[ "$branch" == "$protected" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to get ahead/behind status
get_status() {
    local branch="$1"
    local ahead behind

    ahead=$(git rev-list --count "origin/main..origin/$branch" 2>/dev/null || echo "0")
    behind=$(git rev-list --count "origin/$branch..origin/main" 2>/dev/null || echo "0")

    if [[ $ahead -gt 0 ]] && [[ $behind -gt 0 ]]; then
        echo "⇅ +$ahead -$behind"
    elif [[ $ahead -gt 0 ]]; then
        echo "⇡ +$ahead"
    elif [[ $behind -gt 0 ]]; then
        echo "⇣ -$behind"
    else
        echo "= 0"
    fi
}

# Main script
main() {
    print_info "Fetching latest remote refs from origin..."
    git fetch origin --prune
    print_success "Fetch complete"
    echo

    # Check if main branch exists
    if ! git show-ref --quiet refs/remotes/origin/main; then
        print_error "origin/main does not exist"
        exit 1
    fi

    # Get all remote branches (excluding HEAD)
    print_info "Listing remote branches..."
    branches=$(git branch -r | grep -v HEAD | sed 's|origin/||' | sort)

    if [[ -z "$branches" ]]; then
        print_warning "No remote branches found"
        exit 0
    fi

    # Build list with status for fzf
    declare -a branch_list
    while IFS= read -r branch; do
        status=$(get_status "$branch")
        branch_list+=("$branch | $status")
    done <<< "$branches"

    # Display all branches with status
    print_info "Available branches:"
    printf '%s\n' "${branch_list[@]}"
    echo

    # Use fzf for multi-selection
    print_info "Select branches to delete (use TAB to select multiple, ENTER to confirm):"
    selected=$(printf '%s\n' "${branch_list[@]}" | fzf \
        --multi \
        --preview 'echo {} | awk -F" | " "{print \$1}" | xargs -I {} git log origin/main..origin/{} --oneline' \
        --preview-window=right:50% \
        --header="SPACE: select | TAB: toggle | ENTER: confirm | ESC: cancel" || true)

    if [[ -z "$selected" ]]; then
        print_warning "No branches selected"
        exit 0
    fi

    # Extract branch names from selected items
    declare -a branches_to_delete
    while IFS= read -r line; do
        branch=$(echo "$line" | awk -F' | ' '{print $1}')
        branches_to_delete+=("$branch")
    done <<< "$selected"

    print_info "You have selected ${#branches_to_delete[@]} branch(es) for deletion:"
    for branch in "${branches_to_delete[@]}"; do
        echo "  - $branch"
    done
    echo

    # Check for protected branches
    declare -a protected_found
    declare -a safe_branches
    for branch in "${branches_to_delete[@]}"; do
        if is_protected "$branch"; then
            protected_found+=("$branch")
        else
            safe_branches+=("$branch")
        fi
    done

    if [[ ${#protected_found[@]} -gt 0 ]]; then
        echo
        print_warning "The following branches are protected and will be skipped:"
        for branch in "${protected_found[@]}"; do
            echo "  - $branch"
        done
        echo
    fi

    if [[ ${#safe_branches[@]} -eq 0 ]]; then
        print_error "No safe branches to delete (all selected branches are protected)"
        exit 1
    fi

    # Confirm deletion for each safe branch
    deleted_count=0
    skipped_count=0

    for branch in "${safe_branches[@]}"; do
        echo
        print_info "Branch: $branch"
        status=$(get_status "$branch")
        echo "  Status: $status"
        git log "origin/main..origin/$branch" --oneline -5 2>/dev/null | sed 's/^/    /' || echo "    (no commits ahead of main)"
        echo

        read -p "Delete branch 'origin/$branch'? (y/n): " -n 1 -r confirm
        echo

        if [[ $confirm =~ ^[Yy]$ ]]; then
            if git push origin --delete "$branch" 2>/dev/null; then
                print_success "Deleted origin/$branch"
                ((deleted_count++))
            else
                print_error "Failed to delete origin/$branch"
                ((skipped_count++))
            fi
        else
            print_warning "Skipped origin/$branch"
            ((skipped_count++))
        fi
    done

    # Summary
    echo
    echo "================================================"
    print_success "Operation completed!"
    echo "  Deleted:   $deleted_count"
    echo "  Skipped:   $skipped_count"
    echo "  Protected: ${#protected_found[@]}"
    echo "================================================"
}

# Run main function
main "$@"
