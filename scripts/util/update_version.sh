#! /bin/bash


tag=$1
shift

if [[ -z $tag ]]
then
  echo "ERROR: version number required"
  echo "example: $0 v1.0.1"
  echo "current tags:"
  git tag | cat
  exit 1
fi

function exit_on_error()
{
  echo "There was an error. Commit will not be tagged."
}

trap exit_on_error ERR

set -e
root=$(git rev-parse --show-toplevel)

echo "cd'ing to root directory ($root)"
cd $root

echo "embedding tag in tex2im"
sed "s/^__version__\s*=\s*[\"'][0-9]\+\(\.[-0-9]\+\)*[\"']\s*$/__version__ = '${tag}'/" tex2im -i

echo "looking for pre-tag-release.sh to run"
script=$(find ./ -name 'pre-tag-release.sh')
if [[ -n $script ]]
then
  ${script} "${tag}"
fi

echo "commiting tex2im version bump"
git add tex2im
git commit -m "version bump: ${tag}"
echo "tagging with ${tag}"
git tag -a ${tag}
git tag | grep ${tag}
echo "Successfully tagged commit."


