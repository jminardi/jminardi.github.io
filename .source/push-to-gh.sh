#! /bin/bash

cd ..
ls | egrep -v "CNAME|README.md" | xargs rm -rf
mv .source/output/* .
git status
git add --all .
git commit -m 'rebuild'
git push origin master
