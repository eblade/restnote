" Vim syntax file
" Language: Rest Note Script
" Maintainer: Johan Egneblad
" Latest Revision: 23 August 2014

if exists("b:current_syntax")
  finish
endif

syn match basicLanguageKeywords "^[ ]*\(connect\|template\|fopen\|fclose\|dict\|xml\|raw\|env\|xpath\|xmod\|xadd\|xattr\|xdelete\|until\|sleep\|while\|endwhile\|if\|endif\|sub\|endsub\|setlog\|log\|call\|eval\|return\|fill\|value\|each\|urilist\|list\|namespace\|idle\|every\)"
syn match httpVerbs "^[ ]*\(get\|put\|post\|delete\|xget\|stomp\)"
syn match classTags "^[ ]*\(external\|internal\|use\|include\|attach\|argpop\|argdict\|is\|exit\|repl\)"
syn match debugTags "^[ ]*\(debug\)"

syn match target "->.*$"
syn match variable "([A-Za-z0-9 ]\+)"
syn match comment "%.*$"

let b:current_syntax = "restnote"

hi def link comment Comment
hi def link target Type
hi def link variable Type
hi def link basicLanguageKeywords Statement
hi def link httpVerbs String
hi def link classTags Function
hi def link debugTags Error
