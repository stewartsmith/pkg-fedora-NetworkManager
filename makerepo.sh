#!/bin/bash

set -vx

die() {
	echo "$@" >&2
	exit 1
}

srcdir="$(dirname "$(readlink -f "$0")")"

(test -f $srcdir/NetworkManager.spec \
  && test -f $srcdir/sources) || {
    echo -n "**Error**: Directory "\`$srcdir\'" does not look like the NM pkg dir"
    exit 1
}

# generate the clean dir
fedpkg prep || die "error while \`fedpkg prep\`"

pushd NetworkManager-0.9.9.0
    git init .
    # if you have a local clone of NetworkManager, symlink
    # it as ../.git/local.
    LOCAL_GIT="$(realpath ../.git/local/)"
    if [[ -d "$LOCAL_GIT/" ]]; then
        git remote add local "$LOCAL_GIT/"
        git fetch local
        git fetch local 'refs/remotes/origin/*:refs/remotes/origin/*'
    fi
    git remote add origin git://anongit.freedesktop.org/NetworkManager/NetworkManager
    git commit --allow-empty -m '*** empty initial commit'  # useful, to rebase the following commit
    git add -f -A .
    git commit -m '*** add all'
    cat <<EOF > .gitignore
EOF
    git rm --cached -r .
    git add .
    git commit -m "*** clean state (ignored files removed)"

    REVERT_COUNT="$(echo "${1-1}" | sed -n 's/^\([0-9]\+\)$/\1/p' | head -n1)"
    if [[ "$REVERT_COUNT" != "" ]]; then
        echo "revert the last $REVERT_COUNT commits"
        PATCH_LIST="$(sed -n 's/^Patch\([0-9]\+\): \+\(.*\)$/\1 \2/p' ../NetworkManager.spec | sort -n | tail -n $REVERT_COUNT)"
        echo "$PATCH_LIST"
        # revert and last patches...
        for i in $(seq "$REVERT_COUNT" -1 1); do
            LAST_PATCH_N=$(echo "$PATCH_LIST" | sed -n "$i"'s/^\([0-9]\+\) \+.*$/\1/p')
            LAST_PATCH=$(  echo "$PATCH_LIST" | sed -n "$i"'s/^\([0-9]\+\) \+\(.*\)$/\2/p')
            echo "revert Patch$LAST_PATCH_N \"$LAST_PATCH\"..."
            patch --no-backup-if-mismatch -R -p1 < "../$LAST_PATCH" || die "error reverting Patch$LAST_PATCH_N $LAST_PATCH"
            git add .
            git commit --allow-empty -a -m "<< revert Patch$LAST_PATCH_N \"$LAST_PATCH\""
        done
        BASECOMMIT=`git rev-parse HEAD`
        for i in $(seq 1 "$REVERT_COUNT"); do
            LAST_PATCH_N=$(echo "$PATCH_LIST" | sed -n "$i"'s/^\([0-9]\+\) \+.*$/\1/p')
            LAST_PATCH=$(  echo "$PATCH_LIST" | sed -n "$i"'s/^\([0-9]\+\) \+\(.*\)$/\2/p')
            echo "reapply Patch$LAST_PATCH_N \"$LAST_PATCH\"..."
            # first try git-am to preserve the commit message, otherwise just revert the last commit
            git am "../$LAST_PATCH" || (
                git revert --no-edit $BASECOMMIT~$((i-1))
                COMMIT_MSG="$(git log -n1 --format='%s' $BASECOMMIT~$((i-1)) | sed 's/<< revert \(Patch.*"\)$/>> reapply \1/')"
                git commit --amend -m "$COMMIT_MSG"
            )

            # The tree to the version before should be identical. Just to be sure, reset it.
            git reset $BASECOMMIT~$((i)) -- .
            EDITOR=true git commit --amend --no-edit
            git reset --hard HEAD
        done
    fi
popd


