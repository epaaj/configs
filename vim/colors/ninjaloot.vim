set background=dark
if version > 580
    " no guarantees for version 5.8 and below, but this makes it stop
    " complaining
    hi clear
    if exists("syntax_on")
    	syntax reset
    endif
endif
let g:colors_name="ninjaloot"

hi SpecialKey                       ctermfg=0
hi NonText       cterm=bold	    ctermfg=darkblue
hi Directory                        ctermfg=darkcyan
hi ErrorMsg      cterm=bold	    ctermfg=7		ctermbg=1
hi IncSearch     cterm=NONE	    ctermfg=yellow	ctermbg=green
hi Search        cterm=NONE	    ctermfg=grey	ctermbg=blue
hi MoreMsg                          ctermfg=darkgreen
hi ModeMsg       cterm=NONE	    ctermfg=brown
hi LineNr                           ctermfg=3
hi Question                         ctermfg=green
hi StatusLine    cterm=bold                             ctermbg=0
hi StatusLineNC  cterm=NONE         ctermfg=darkgray    ctermbg=0
hi VertSplit     cterm=NONE         ctermfg=darkgray    ctermbg=0
hi Title                            ctermfg=5
hi Visual        cterm=reverse
hi VisualNOS     cterm=bold,underline
hi WarningMsg			    ctermfg=1
hi WildMenu			    ctermfg=0		ctermbg=3
hi Folded			    ctermfg=darkgray	ctermbg=none
hi FoldColumn			    ctermfg=3   	ctermbg=none
hi DiffAdd						ctermbg=4
hi DiffChange						ctermbg=5
hi DiffDelete    cterm=bold	    ctermfg=4		ctermbg=6
hi DiffText      cterm=bold				ctermbg=1
hi Comment			    ctermfg=darkgray
hi Constant			    ctermfg=3
hi Special			    ctermfg=5
hi Identifier			    ctermfg=5
hi Statement			    ctermfg=3
hi PreProc			    ctermfg=6
hi Type				    ctermfg=2
hi String			    ctermfg=1
hi Underlined    cterm=underline    ctermfg=5
hi Ignore			    ctermfg=darkgrey
hi Error         cterm=bold	    ctermfg=7		ctermbg=1
hi LineNr			    ctermfg=darkgrey

"vim: sw=4
