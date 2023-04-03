## To change the date:
```bash
GIT_COMMITTER_DATE="Wed, 23 Oct 2019 17:40:24 +0500" git commit --amend --no-edit --date "Wed, 23 Oct 2019 17:40:24 +0500"
```

## Unset option
[Link](https://stackoverflow.com/questions/11868447/how-can-i-remove-an-entry-in-global-configuration-with-git-config)
```bash
$ git config --global --unset core.autocrlf
```



# Vim relate commands
## CRLF -> LF
Learn more?
### Example 1
Didn't work, file still has `\r`, where `eacon` is defined in file `.env` `export DATABASE_USER='eacon'`
```
Access denied for user 'eacon\r'@'localhost' (using password: YES)")
```
[Link](https://stackoverflow.com/questions/48692741/how-can-i-make-all-line-endings-eols-in-all-files-in-visual-studio-code-unix)
```bash
$ git config core.autocrlf false

$ git rm --cached -r .         # Don’t forget the dot at the end

$ git reset --hard
```
```

```
## Something with argdo in vim
- This will change occurence of /usr/bin/bash
```
:argdo set ff=unix | update#!/usr/bin/bash
```
