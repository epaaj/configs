nmap gbi oif [] ; then<return>else<return>fi<esc><<2k2la
nmap gbf ofor i in ``; do<return>echo $i<return>done<esc><<2k6la
nmap gbc ocase "" in<return><tab>*)<return><tab>echo<return>;;<return><bs><bs>esac<esc>4k2la
nmap gbw owhile ; do<return>echo<return>done<esc><<2k2la
nmap gbF o} # }}}<esc>O<tab>echo<esc>O() { # {{{<esc>I
