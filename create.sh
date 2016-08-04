#!/bin/sh

pushd skill
zip -r skill.zip . -x *.swp*
popd
mv skill/skill.zip .
