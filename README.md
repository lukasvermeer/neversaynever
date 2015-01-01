Never Say Never [#SaidNoOneEver](https://twitter.com/search?q=%23SaidNoOneEver)
=============

[Johan envisioned](https://twitter.com/jugander/status/534178436453900288) a Twitter bot that introduces people who say "X, said no one ever" to people who've said X.

[Lukas](http://www.lukasvermeer.nl) made a thing that does something like that.

You can see the result in action [here](lukasvermeer.nl/projects/neversaynever/).

# Setup webserver

Just upload the .html and .css files to some path on your webserver.

# Update script

Create a file name update_json.sh somewhere that contains the following.

    python /PATH/___snoe.py -f LOGFILE -k CONSUMER_KEY -s CONSUMER_SECRET >> LOGFILE
    ( echo "["; sed -e 's/$/,/' LOGFILE; echo "]" ) > /PATH/tweets.json
    scp /PATH/tweets.json SERVER:SERVER_PATH/.

Setup your crontab to execute the script at regular intervals.

    */5 * * * * /PATH/update_json.sh
