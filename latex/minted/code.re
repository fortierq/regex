[ ]*\\begin\{minipage\}\{.*\\textwidth\}
[ ]*\\begin\{minted\}\[.*\]\{.*\}
(([^\\]|\n)*)
[ ]*\\end\{minted\}
[ ]*\\end\{minipage\}

\begin{code}{python}
$1
\end{code}
