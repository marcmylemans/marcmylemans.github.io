---
layout: post
title: Remote Desktop Services, Set up email discovery to subscribe to your RDS feed
categories: Windows Server
tags: server 2022 rdp webfeed
---

i'm writing this small guile in extension of the Remote Desktop series.

You can use your e-mail to 'autodiscover' your remote desktop webfeed. (like your exchange autodiscover record).

i'm going to use contoso.com as our example here and your users get an e-mail in the form of firstname.lastname@contoso.com

For this to work you need to create a new TXT record on your public nameservers that points to your Remote desktop Webfeed.

The value for the new TXT record:

```
_msradc
```

Text value:

```
https://gatewayserver.contoso.com/RDWeb/FeedLogin/WebFeedLogin.aspx
```

If you have done everything correctly you should be able to resolve this record with nslookup:

```
nslookup _msradc.contoso.com
```


Be sure to check out the previous video where we configured Remote Desktop Services:

[Server 2022 - Remote Desktop Services - Part 1]({% link _posts/2022-12-27-RemoteDesktopPart1.md %})

[Server 2022 - Remote Desktop Services - Part 2]({% link _posts/2022-12-31-RemoteDesktopPart2.md %})

[Server 2022 - Remote Desktop Services - Part 3]({% link _posts/2023-01-03-RemoteDesktopPart3.md %})

[Installing Office 365 on a Remote Desktop Host!]({% link _posts/2023-01-04-RemoteDesktopPart4.md %})

[Server 2022 - Remote Desktop Services - Part 5]({% link _posts/2023-01-05-RemoteDesktopPart5.md %})

[Server 2022 - Remote Desktop Services - Part 6]({% link _posts/2023-01-23-Remote_DesktopPart6.md %})

[Server 2022 - Remote Desktop Services - Part 7]({% link _posts/2023-01-23-Remote_DesktopPart7.md %})