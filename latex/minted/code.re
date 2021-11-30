[ ]*\\begin\{minipage\}\{.*\\textwidth\}
[ ]*\\begin\{minted\}\[.*\]\{(.*)\}
(([^\\]|\n)*)
[ ]*\\end\{minted\}
[ ]*\\end\{minipage\}

\begin{code}{$1}
$2
\end{code}
