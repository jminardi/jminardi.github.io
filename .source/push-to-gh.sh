#! /bin/bash

make html
cd ..
ls | grep -v CNAME | xargs rm -rf
mv .source/output/* .
git status
git add .
git commit -m 'rebuild'
git push origin master
