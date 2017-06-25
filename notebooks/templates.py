slide_template = r"""
\begin{{frame}}[fragile]
\frametitle{{{title}}}
\vspace{{1em}}

\emph{{{query}}}

\vfill

\begin{{table}}
  \centering
  \begin{{tabular}}{{ l l l l }}
    & \textbf{{Amy}} & \textbf{{Sarah}} & \textbf{{Martin}}\\
    \toprule
    {rows}
    \bottomrule
  \end{{tabular}}
\end{{table}}

\vfill

\tiny{{

\begin{{enumerate}}
\item Is this query best answered with a pin on a map?
\item Is a location explicit in the query?
\item What type of query is this?
\end{{enumerate}}

\vfill

\begin{{multicols}}{{2}}
\begin{{verbatim}}
YY = Yes -- with place name
YN = Yes -- without place name
NY = No (but still a place)
NN = Not applicable 
     (ie not explicit location and not a place)
\end{{verbatim}}

\columnbreak
\begin{{verbatim}}
IAD = INFORMATIONAL_ADVICE
IDC = INFORMATIONAL_DIRECTED_CLOSED
IDO = INFORMATIONAL_DIRECTED_OPEN
ILI = INFORMATIONAL_LIST
ILO = INFORMATIONAL_LOCATE
IUN = INFORMATIONAL_UNDIRECTED
NAV = NAVIGATIONAL
RDE = RESOURCE_ENTERTAINMENT
RDO = RESOURCE_DOWNLOAD
RIN = RESOURCE_INTERACT
ROB = RESOURCE_OBTAIN
\end{{verbatim}}
\end{{multicols}}
}}

\end{{frame}}
"""
