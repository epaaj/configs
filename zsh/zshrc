# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000

setopt extendedglob
bindkey -e

# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '~/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall

if [ -f ~/.aliasrc ] ; then
	source ~/.aliasrc
fi

autoload colors zsh/terminfo
if [[ "$terminfo[colors]" -ge 8 ]]; then
	colors
fi
for color in BLACK RED GREEN YELLOW BLUE MAGENTA CYAN WHITE; do
	eval PR_$color='%{$terminfo[bold]$fg[${(L)color}]%}'
	eval PR_LIGHT_$color='%{$fg[${(L)color}]%}'
	(( count = $count + 1 ))
done
NC="%{$terminfo[sgr0]%}"

if [ `id -u` = 0 ] ; then
	eval D=$PR_RED
	eval L=$PR_LIGHT_RED
else
	if [[ $HOST = "infinitus" || $HOST = "loltop" || $HOST = "mumsig" ]] ; then
		eval D=$PR_BLACK
		eval L=$PR_LIGHT_BLACK
	elif [[ $HOST = "ninjaloot" ]] ; then
		eval D=$PR_CYAN
		eval L=$PR_LIGHT_CYAN
	fi
fi

PROMPT="$D┌─[${PR_GREEN}%n@%m$D]-[${PR_BLUE}%~$D]
$D└─[$PR_CYAN%*$D]$L>$NC "
