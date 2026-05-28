cd /c/code/temp/astro-bookings-copilot-4 && 
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD) && echo "CURRENT_BRANCH:$CURRENT_BRANCH" && 
STATUS=$(git status --porcelain) && if [ -n "$STATUS" ]; then echo "UNCOMMITTED_CHANGES:true"; else echo "UNCOMMITTED_CHANGES:false"; fi && 
git fetch origin && 
if git ls-remote --heads origin main | grep -q refs/heads/main; then DEFAULT_BRANCH=main; else DEFAULT_BRANCH=master; fi && echo "DEFAULT_BRANCH:$DEFAULT_BRANCH" && 
# checkout default branch
git checkout $DEFAULT_BRANCH && 
# pull latest
git pull origin $DEFAULT_BRANCH && 
# merge current branch
git merge --no-ff $CURRENT_BRANCH -m "chore: merge branch $CURRENT_BRANCH into $DEFAULT_BRANCH" && 
# push merge
git push origin $DEFAULT_BRANCH