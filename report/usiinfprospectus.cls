%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% LaTeX class for the PhD prospectus at the Faculty of Informatics of Universita' della Svizzera Italiana
% 
% Contributors:
% Andrea Adamoli, Domenico Bianculli, Michele Lanza (original design), Jochen Wuttke
%
%
% -----------------------------------------------------------------------------
%%
%% This file is 'USIINFprospectus.cls'
%% 
%% It may be distributed and/or modified under the conditions of the LaTeX Project Public License, either version 1.3c of this license or (at your option) any later version. The latest version of this license is in http://www.latex-project.org/lppl.txt and version 1.3c or later is part of all distributions of LaTeX version 2005/12/01 or later.

%%% identification
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{usiinfprospectus}[2009/11/06 v. 1.1%
  USI Informatics Prospectus class]
%%% initial code
\RequirePackage{xifthen}
%%% true to produce a version suitable for printing
\newboolean{@printversion}
%%% true to enable automatic loading of hyperref package
\newboolean{@hypermode}
%%% true if a subtitle is provided
\newboolean{@subtitle}
%%% declaration of options
\DeclareOption{print}{\setboolean{@printversion}{true}}
  {%redefine margins to match oneside layout
  }
%%% enable/disable hyperref
\DeclareOption{hyper}{\setboolean{@hypermode}{true}}
\DeclareOption{nohyper}{\setboolean{@hypermode}{false}}

\DeclareOption{a5paper}{\OptionNotUsed}
\DeclareOption{letterpaper}{\OptionNotUsed}
\DeclareOption{b5paper}{\OptionNotUsed}
\DeclareOption{legalpaper}{\OptionNotUsed}
\DeclareOption{executivepaper}{\OptionNotUsed}
\DeclareOption{landscape}{\OptionNotUsed}
\DeclareOption{openany}{\OptionNotUsed}
\DeclareOption{twocolumn}{\OptionNotUsed}
\DeclareOption{oneside}{\OptionNotUsed}
\DeclareOption{twoside}{\OptionNotUsed}

%%%
\DeclareOption*{% 
\PassOptionsToClass{\CurrentOption}{document}% 
} 
%%% execution of options
\ExecuteOptions{hyper}
\ProcessOptions \relax
\typeout{*** Please report bugs, comments, suggestions, and improvements
  to: }
\typeout{*** Domenico Bianculli <domenico.bianculli@usi.ch>}
%%% package loading
\LoadClass[a4paper,10pt,twoside,onecolumn,final,titlepage,top=0.2]{article}
%%% main code

%font settings
\RequirePackage[T1]{fontenc}
\RequirePackage[charter]{mathdesign}
\RequirePackage[scaled]{beramono}
\renewcommand{\sfdefault}{uop}
\renewcommand{\scshape}{%
\not@math@alphabet\scshape\relax
\ifthenelse{\equal{\f@family}{uop}}%
{\fontshape{sc}\selectfont}%
{\fontshape{fsc}\selectfont}%
}


%sans-serif titles
\RequirePackage{sectsty}
\allsectionsfont{\normalfont}

%geometry
\RequirePackage[a4paper,total={170mm,257mm}]{geometry}
\geometry{hscale=0.67}
\ifthenelse{\boolean{@printversion}}{}%
{  \geometry{asymmetric}
  \geometry{bindingoffset=0pt,hmarginratio=1:1}
}

%%% fancy headers
\RequirePackage{fancyhdr}
\setlength{\headheight}{15pt}
\fancypagestyle{cover}{%
\fancyhf{}
 \fancyhead{\mbox{ }}
}
\fancypagestyle{hrulefpage}{%
 \fancyhf{}
  \fancyhead{\mbox{ }}
  \fancyfoot[C]{\thepage}
}
%modifying captions
\RequirePackage[font=footnotesize,labelsep=period,sc]{caption}
\setlength{\captionmargin}{30pt}
%datatool
\RequirePackage{datatool}
\RequirePackage{calc}

%commands to print empty values in the database 
\newcommand{\print@blank}[1]{\ifthenelse{\equal{#1}{!blank!}}{}{#1\ }}
\newcommand{\print@empty}[1]{\ifthenelse{\equal{#1}{!blank!}}{}{#1}}

%utilities
\newcommand{\TODO}[1]{\noindent{\textbf{TODO: #1}}}
\newcommand{\CONTRIBUTION}[1]{
\hspace{-0.82cm}
\begin{tabular}{p{3.85cm}p{12.7cm}}
\textbf{Envisioned contribution:}&{#1}
\end{tabular}
}
\newcommand{\PATI}[1]{\vspace{0.1cm}\textbf{#1}}

%%% additional titlepage content commands
\newcommand{\subtitle}[1]{\gdef\@subtitle{#1}\setboolean{@subtitle}{true}}
\renewcommand\abstract[1]{\def\@abstract{\\#1}}
%%% submission and acceptance dates
%%% true if the dissertation has been accepted
\newboolean{@accepted}
\newcommand{\versiondate}[1]{\setboolean{@accepted}{true}\gdef\@dateaccepted{#1}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%% TITLE PAGE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%% PAGE HEADER %%%%%%%%%%%%%%%%

\renewcommand{\maketitle}{%
\pagenumbering{Alph}\begin{titlepage}
\thispagestyle{empty}
\noindent \includegraphics[width=123mm]{logo-info.pdf}
\hspace{-0.8mm}\rule[3.6mm]{\textwidth-123mm}{0.2pt}
\vspace{-20mm}
\begin{flushright}
{\Large \textsf{Theory of Computation 2021}}
\end{flushright}
\vspace{1mm}
\hfill {%
\ifthenelse{\boolean{@accepted}}{%
\textsf{\@dateaccepted}%
}{%
\textsf{Submitted on \@datesubmitted}%
}%
}\\
\vspace{16mm}

%%%%%%%%%%%%%%%% TITLE, SUBTITLE, AUTHOR %%%%%%%%%%%%%%%%

%%% TITLE %%%
\noindent {\huge {\textsf{\@title}}}
%%% (OPTIONAL SUBTITLE) %%%
\ifthenelse{\boolean{@subtitle}}{ \noindent{\large \\[0.5em]\textsf{\textbf{\@subtitle}}}\\[12mm]}{\\[12mm]}
%%% AUTHOR %%%
\hfill { \Large {\textsf{\textbf{\@author}}}}\\

%%%%%%%%%%%%%%%% ABSTRACT %%%%%%%%%%%%%%%%

\hrule height 0.2pt  \vspace{4mm}
\noindent{{\Large{Project}}}\\ 
\@abstract
\vfill \hrule height 0.2pt \vspace{3mm}

%%%%%%%%%%%%%%%% RESEARCH ADVISOR AND EVENTUAL CO-ADVISORS %%%%%%%%%%%%%%%%

\end{titlepage}
\setcounter{footnote}{0}
}

\renewenvironment{titlepage}
    {%
      \cleardoublepage
      \pagenumbering{arabic}
      \setcounter{page}\z@
    }%
    {\newpage }
        {\textwidth 5cm}
  
%%% put ToC, LoF, LoT and Index entries in the ToC use of \phantomsection is required for dealing with the hyperref package and depends on the nohyper option

%%% other useful packages

\RequirePackage{booktabs}
\RequirePackage{graphicx}
\RequirePackage{textcomp}
\RequirePackage{url}
\RequirePackage{amsmath}
%%% switch on hyperref support
\ifthenelse{\boolean{@hypermode}}{%
\RequirePackage[unicode,plainpages=false,pdfpagelabels,breaklinks]{hyperref}
\RequirePackage[all]{hypcap}

}{}

%%% other formatting stuff

\renewcommand{\baselinestretch}{1.05}
