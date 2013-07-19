#! /bin/bash

cd ..
ls | grep -v "CNAME README.md" | xargs rm -rf
mv .source/output/* .
git status
git add .
git commit -m 'rebuild'
git push origin master
