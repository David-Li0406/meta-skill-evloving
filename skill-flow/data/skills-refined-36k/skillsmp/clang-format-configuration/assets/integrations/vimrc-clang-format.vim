" Vim configuration for clang-format integration
" Format on save for C++ files

" Python 3 support
if has('python3')
  map <C-K> :py3f /path/to/clang-format.py<cr>
  imap <C-K> <c-o>:py3f /path/to/clang-format.py<cr>
endif

" Python 2 support
if has('python')
  map <C-K> :pyf /path/to/clang-format.py<cr>
  imap <C-K> <c-o>:pyf /path/to/clang-format.py<cr>
endif

" Format on save
function! Formatonsave()
  let l:formatdiff = 1
  py3f /path/to/clang-format.py
endfunction
autocmd BufWritePre *.h,*.cc,*.cpp call Formatonsave()
