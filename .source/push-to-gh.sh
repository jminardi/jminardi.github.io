#! /bin/bash

cd ..
ls | grep -v CNAME | xargs -rf
mv .source/output/* .
git add .
git commit -m 'rebuild'
git push origin master


#rm -rf .old-gh-pages
#mv gh-pages .old-gh-pages
#cp -r output/ gh-pages/
#cp -r .old-gh-pages/.git gh-pages/.git
#cp  .old-gh-pages/CNAME gh-pages/CNAME
#cd gh-pages
#git add .
#git commit -m
#git push origin master
#cd ..
#rm -rf .old-gh-pages
