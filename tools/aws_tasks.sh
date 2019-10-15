#!/usr/bin/env bash

# This script is used on main repo via travis.
# It enables travis jobs to store builds on S3 for release packaging

function setup {
    mkdir -p "$HOME/$TRAVIS_BUILD_NUMBER"
    x_aws_credentials
    x_aws_install
}

function synchronize_down {
    aws s3 sync s3://fritzing/"$TRAVIS_BUILD_NUMBER" "$HOME/$TRAVIS_BUILD_NUMBER"
}

function synchronize_up {
    aws s3 sync "$HOME/$TRAVIS_BUILD_NUMBER" s3://fritzing/"$TRAVIS_BUILD_NUMBER"
}

function cleanup {
    aws s3 rm --recursive s3://fritzing/"$TRAVIS_BUILD_NUMBER" # clean up after ourselves
}

function store_with_md5 {
    cp "$1/$2" "$HOME/$TRAVIS_BUILD_NUMBER"
    md5sum "$HOME/$TRAVIS_BUILD_NUMBER/$2" > "$HOME/$TRAVIS_BUILD_NUMBER/$2.md5"
}

function x_aws_install {
    case "$TRAVIS_OS_NAME" in
        linux*)
            pip install --user awscli
            ;;
        osx*)
            pip3 install --user awscli
            ;;
        windows*)
            choco install awscli
            ;;
    esac
}

function x_aws_env {
    case "$TRAVIS_OS_NAME" in
        linux*)
            export PATH=$HOME/.local/bin:$PATH
            ;;
        osx*)
            export PATH=$HOME/Library/Python/3.7/bin:$PATH
            ;;
        windows*)
            export "PATH=/c/Program Files/Amazon/AWSCLI/bin:$PATH"
            ;;
    esac
}

function x_aws_credentials {
    mkdir -p "$HOME"/.aws
    cat > "$HOME"/.aws/credentials << EOL
[default]
aws_access_key_id = ${AWS_ACCESS_KEY_ID}
aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}
EOL
}

if [[ ( "$TRAVIS_PULL_REQUEST" == false ) && ( "$TRAVIS_BRANCH" == "develop" || "$TRAVIS_BRANCH" == "master" ) && ( "$TRAVIS_REPO_SLUG" == "fritzing/fritzing-app" )]]; then
    x_aws_env

    echo "Running deploy task '$1' on $TRAVIS_OS_NAME ( $OSTYPE )"
    "$@"
fi
