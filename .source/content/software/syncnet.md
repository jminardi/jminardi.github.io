title: SyncNet: A Decentralized Web Browser
date: 15/1/2014

<a href='http://en.wikipedia.org/wiki/File:A_wedge_of_starlings_-_geograph.org.uk_-_1069366.jpg' id='borderless'>
![](|filename|/images/syncnet/bird-flock.png)
</a>

Imagine if we lived in a world where more demand meant less load for a
webserver. Imagine if we lived in a world where no organization could take down
a website, and everyone could publish a site with no hassle or upfront cost.
[SyncNet][0] is a first step into that world.

[SyncNet][0] is an experimental new browser built on top of BitTorrent Sync and
(soon) Colored Coins. Every time you access a site, you store all of its
contents on your machine. The next user to request the site can get the
contents from both your machine and the original server. As more people access
a page, it becomes available from more machines, reducing the load on the
original server.

Technology
----------
SyncNet uses BitTorrent Sync to handle distributing the content of a site and
Colored Coins to handle domain resolution. (Colored Coins not implemented yet.)

### BitTorrent Sync

[BitTorrent Sync][2] uses the BitTorrent protocol to keep directories in sync across
the internet, much like DropBox. Say you have two folders that you want to keep
in sync, one at home and one at work. On one of the computers you add the
directory to BTSync, and it will give you a "secret".  (A secret is a string of
33 characters - 160 bits encoded in base32) Now on the other computer you add a
new folder using the same secret and they will stay in sync as long as they are
both connected to the internet. BTSync works behind the scenes breaking up your
files into little chunks and pushes the changes between both computers, and it
does this all without requiring a central server like DropBox does.

Along with the secrets mentions above, BTSync also lets you generate "read only
secrets". If you share your read only secret with someone they will be able to
download your files, but they will not be able to make changes that will be
synced back to your computer. Every secret has a corresponding read only
secret.

[2]: http://www.bittorrent.com/sync

### Colored Coins

[Colored Coins][1] are a new idea that enable "smart property" and are
implemented on top of the BitCoin protocol. Colored Coins essentially allow you
to _color_ a certain coin and mark that it represents ownership of something
else. In SyncNet a colored coin will represent ownership of a domain name.
Anyone with access to the Bitcoin blockchain (which is public data) will be
able to see who owns a domain name and what secret it resolves to.

The current implementation of SyncNet does not use Colored Coins, but that
should be coming soon.

[1]: https://docs.google.com/a/minardi.org/document/d/1AnkP_cVZTCMLIzw4DvsW6M8Q2JC0lIzrTLuoWu2z1BE/edit

### Tying it together

You can probably see where this is going. All SyncNet does is use BTSync to
fetch a directory of HTML files and then renders them for the user. If those
HTML files include a hyperlink to a URL starting with `sync://<secret>` then
that secret will be added and the contents of the new directory will be
displayed.

Because all the heavy lifting is done by BTSync and a QWebView, SyncNet itself
is quite small. You can browse all the source code on [github][0].

[0]: https://github.com/jminardi/syncnet

User Interface
--------------
Here is a screen shot of the current SyncNet user interface:

<a href='/images/syncnet/main-screen-shot.png', id='borderless'>
<img src='/images/syncnet/main-screen-shot.png' id='borderless' width=550>
</a>

I am serving the website you are currently reading under the read only secret
`B4KWMK3VBJSH35YZMS7ZEMSQ6XNVBHALY`

Entering that secret in the URL bar of SyncNet will cause it to fetch my whole
site and display the index page. Now any time I update my website the changes
will be synced to anyone who has downloaded it. SyncNet monitors the directory
and refreshes the page if any changes are detected. This is useful because if
anyone with a read/write secret makes changes to the pages, all connected
clients will quickly reflect that change.

To add your own content to SyncNet you just need to add a directory of HTML
files to BitTorrent Sync. This can be accomplished in SyncNet easily by
clicking the plus icon in the top right. That will open up the following
dialog:

<img src='/images/syncnet/new-site.png' id='borderless'>

Using this dialog you can create a new SyncNet site. You must generate your
secret from a seed, which is just a string of characters. Anyone who knows this
seed will be able to recover your secret. And remember, anyone with your secret
is able to modify the contents of your site. So keep this seed secret! (And
keep your secret secret!)

Once you are satisfied with your seed, click "Ok" and your new SyncNet site
will be added. A directory should pop up, and if you drop HTML files into this
folder, they will be served to anyone who requests your page.

Caveats
-------

SyncNet only works with static content. This means no social networks or other
dynamic content. However many sites today do not need to be dynamic and would
benefit from converting to only static resources. Most blogs or news sites
could be served with SyncNet with little to no modifications.

Another caveat is long load times. This is because SyncNet needs to pull down
all files for a requested site, not only those needed to render the current
page. However BTSync has selective sync capabilities so this could be improved
in the future. At the very least ensuring that the index page is synced first
would go a long way in speeding things up.

Future Work
-----------

As mentioned above, a major missing piece is domain resolution. This will be
implemented with Colored Coins (or something similar such as namecoins.)

It would also be nice to be able to create a sync site from any WWW site that
currently exists. Browse to a page you like in SyncNet, click on a single
button and convert the site to a new SyncNet site.

Another future goal is to implement SyncNet as a chrome or firefox plugin,
where a whole separate browser is not needed. This may be possible in the
future.

Conclusion
----------

I was pretty happy with how little work it ended up being to tie these
technologies together into SyncNet. While SyncNet may not be the implementation
that exists into the future, I believe it is a step down the path that the
internet seems to be going. Decentralizing more and more aspects of the core
technologies of the internet will make it more robust in the face of targeted
attacks and censorships attempts.

If you like these ideas feel free to submit a pull request on [github][0] or
reach out to me on [twitter][4].

[4]: http://twitter.com/jackminardi
