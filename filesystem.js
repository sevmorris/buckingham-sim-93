export const FS = {

  /* ── System directories ───────────────────────────────────────────────── */
  '/': {
    type:'dir', perms:'drwxr-xr-x', owner:'root', group:'wheel',
    size:160, mtime:'Sep 28 12:00'
  },
  '/home': {
    type:'dir', perms:'drwxr-xr-x', owner:'root', group:'wheel',
    size:60, mtime:'Sep 28 12:00'
  },
  '/mnt': {
    type:'dir', perms:'drwxr-xr-x', owner:'root', group:'wheel',
    size:60, mtime:'Oct  5 09:12'
  },
  '/tmp': {
    type:'dir', perms:'drwxrwxrwt', owner:'root', group:'wheel',
    size:40, mtime:'Oct  5 09:14'
  },

  /* ── Home directory ───────────────────────────────────────────────────── */
  '/home/joe': {
    type:'dir', perms:'drwxr-xr-x', owner:'joe', group:'staff',
    size:512, mtime:'Oct  5 09:14'
  },

  '/home/joe/.cshrc': {
    type:'file', perms:'-rw-r--r--', owner:'joe', group:'staff',
    size:291, mtime:'Oct  3 22:17', hidden:true,
    content:
`# .cshrc -- joe@owl
set path = (/usr/ucb /usr/bin /bin /usr/local/bin /usr/openwin/bin .)
set prompt = "joe@owl% "
set history = 100
set savehist = 50
set ignoreeof
setenv TERM xterm
setenv EDITOR vi
setenv PAGER more
setenv DISPLAY :0.0
alias h      history
alias j      jobs
alias ll     'ls -la'
alias rm     'rm -i'
alias mail   elm
alias bye    logout`
  },

  '/home/joe/.plan': {
    type:'file', perms:'-rw-r--r--', owner:'joe', group:'staff',
    size:89, mtime:'Oct  4 18:30', hidden:true,
    content:
`Finishing CIS 4707 (Compiler Design).  Thinking about grad school apps.
Looking for a roommate -- near campus, $350/mo, avail Nov 1.
Ask me about PowerPC vs x86.  I have opinions.`
  },

  '/home/joe/notes.txt': {
    type:'file', perms:'-rw-r--r--', owner:'joe', group:'staff',
    size:498, mtime:'Sep 30 14:22',
    content:
`terminal setup notes
Oct 1993

buckingham is installed in /usr/local/bin -- just type  buckingham  to run it.
/mnt/floppy has some old scripts and a backup copy.

elm works for mail.  pine might be better.  Still deciding.
Mosaic 2.0 is on /usr/local/bin -- DNS is slow, be patient.`
  },

  '/home/joe/todo': {
    type:'file', perms:'-rw-r--r--', owner:'joe', group:'staff',
    size:247, mtime:'Oct  5 08:55',
    content:
`[ ] CIS 4707 compiler project -- due friday (shift-reduce conflicts)
[ ] return books to Paley Library (Tanenbaum, Stevens APUE)
[ ] ask about thesis extension
[ ] figure out why Mosaic dumps core on .gif images
[x] install buckingham to /usr/local/bin`
  },

  /* ── Letters directory ────────────────────────────────────────────────── */
  '/home/joe/letters': {
    type:'dir', perms:'drwx------', owner:'joe', group:'staff',
    size:128, mtime:'Oct  5 09:00'
  },

  /* ── Letter files ────────────────────────────────────────────────────── */
  '/home/joe/letters/letter_001.txt': {
    type:'file', perms:'-rw-------', owner:'joe', group:'staff',
    size:512, mtime:'Oct  1 14:22',
    content:
`October 1, 1993

[Your first letter goes here.

Replace this placeholder text with whatever you'd like to share.
Save the file, reload, and the letter will appear to anyone
who logs in.]`
  },

  '/home/joe/letters/letter_002.txt': {
    type:'file', perms:'-rw-------', owner:'joe', group:'staff',
    size:512, mtime:'Oct  3 20:11',
    content:
`October 3, 1993

[Second letter placeholder.  Add as many letter files as you like.
Copy one of the existing entries in the FS object above and
give it a new path, mtime, and content.]`
  },

  /* ── Local binaries ──────────────────────────────────────────────────── */
  '/usr/local': {
    type:'dir', perms:'drwxr-xr-x', owner:'root', group:'wheel',
    size:64, mtime:'Oct  5 09:00'
  },
  '/usr/local/bin': {
    type:'dir', perms:'drwxr-xr-x', owner:'root', group:'wheel',
    size:128, mtime:'Oct  5 09:00'
  },
  '/usr/local/bin/buckingham': {
    type:'file', perms:'-rwxr-xr-x', owner:'root', group:'wheel',
    size:1024, mtime:'Oct  5 09:00',
    content:
`#!/bin/csh -f
# buckingham -- a text adventure`
  },

  /* ── Floppy disk ──────────────────────────────────────────────────────── */
  '/mnt/floppy': {
    type:'dir', perms:'drwxr-xr-x', owner:'root', group:'wheel',
    size:64, mtime:'Oct  5 09:12'
  },

  '/mnt/floppy/README.txt': {
    type:'file', perms:'-rw-r--r--', owner:'root', group:'wheel',
    size:312, mtime:'Oct  5 09:12',
    content:
`BUCKINGHAM  --  A Text Adventure
------------------------------

A small game. A room. Some things left behind.

To play:
  buckingham

Commands inside the game:
  look            describe the room
  take <item>     pick something up
  drop <item>     put it back down
  read <item>     read it
  examine <item>  look more closely
  inventory       list what you're carrying
  quit            return to the shell`
  },

  '/mnt/floppy/buckingham': {
    type:'file', perms:'-rwxr-xr-x', owner:'root', group:'wheel',
    size:512, mtime:'Oct  5 09:12',
    content:
`#!/bin/csh -f
# buckingham -- backup copy
# see /usr/local/bin/buckingham for the installed version
exec /usr/local/bin/buckingham`
  },

};