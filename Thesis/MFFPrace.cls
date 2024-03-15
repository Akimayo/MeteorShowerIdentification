\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{./MFFPrace}[2024/02/08 MFF Bakalářské práce a studentské projekty]

% =-=-=-=             DOKUMENTACE             =-=-=-=
% - ADRESÁŘOVÁ STRUKTURA A NAČTENÍ TŘÍDY
%       TeX bude pro tuto třídu očekávat následující
%     strukturu adresářů:
%     +-----------------------------------+
%     |    <adresar projektu>             |
%     |    ├ img                          |
%     |    | └ logo-cs.pdf                |
%     |    ├ <nazev dokumentu>.tex        |
%     |    └ MFFPrace.cls                 |
%     +-----------------------------------+
%     `<adresar projektu>` a `<nazev dokumentu>` jsou
%     libovolné. `logo-cs.pdf` je přiloženo a
%     `MFFPrace.cls` je tento soubor.
%       Třídu načtete z `<nazev dokumentu>.tex` pomocí
%     >   \documentclass[<argumenty>]{./MFFPrace}
%     kde `<argumenty>` jsou popsány níže.
% - PŘÍPADY UŽITÍ
%     * Studentský projekt (jednodušší)
%           Vytvoří formátovaný dokument s minimálními
%         informacemi pro účely studentského projektu.
%         Vyžaduje pouze parametry v poslední sekci
%         označené "▘". Volitelně mohou být použity
%         také parametry označené "▖"
%           Pro tento případ použijte argument
%         třídy [project], doporučen je také argument
%         [twoside], který udělá dokument oboustranný.
%     * Bakalářská práce (plná)
%           Vytvoří dokument dle náležitostí
%         bakalářských prací na MFF UK. Vyžaduje
%         nastavení všech parametrů v poslední sekci.
%           Pro tento případ není potřeba předávat
%         třídě žádné argumenty. Automaticky bude
%         dokument jednostranný, v případě potřeby je
%         však možné také použít argument [twoside].
% - TITULNÍ STRANA
%       Třída předefinovává makro `\maketitle` tak,
%     aby vygenerovalo potřebné formální prvky na
%     úvodu dokumentu. Použijte jej ihned po otevření
%     prostředí dokumentu.
% - UŽITEČNÁ MAKRA
%     * Vlastní poznámky
%           Makra pro vkládání dočasných poznámek do
%         textu. Tyto poznámky jsou zvýrazněné barvou
%         a ikonkou a jsou skryta při použití
%         argumentu `final`.
%           × \todo{<poznámka>}
%           × \note{<poznámka>}
%           × \ask{<poznámka>}
%     * Seznam úkolů
%           Seznam se zaškrtávacími políčky, který se
%         skryje při použití argumentu `final`.
%           Příklad použití:
%         ```
%         \begin{todolist}
%           \item Rozpracovaný úkol
%           \item[\done] Dokončený úkol
%           \item[\wontfix] Zrušený úkol
%         \end{todolist}
%         ```
%     * Kapitola bez čísla
%           Šablona bakalářské práce udává, že úvod a
%         závěr práce by neměly být číslované, ale
%         musejí se objevit v obsahu. K tomu slouží
%         makro \chapwithtoc{<název kapitoly>}.
%     * Další makra pro matematiku a programování
%           Šablona bakalářské práce obsahuje další
%         makra pro usnadnění sázení matematických
%         důkazů, počítačového kódu a dalších. Tyto
%         naleznete i s původními komentáři na konci
%         tohoto souboru.
% - PARAMETRY
%     * \NazevPrace{Název bakalářské práce či studentského projektu dle zadání}▘
%     * \NazevPraceEN{Název v anglickém jazyce dle zadání}
%     * \AutorPrace{Jméno autora}▘
%     * \RokOdevzdani{Rok odevzdání práce}▘
%     * \Katedra{Katedra, na které je práce zpracovávána}▘
%     * \KatedraEN{Katedra v anglickém jazyce}
%     * \TypPracoviste{Typ pracoviště, např. katedra, laboratoř, oddělení}
%     * \TypPracovisteEN{Typ pracoviště v anglickém jazyce}
%     * \Vedouci{Jméno vedoucí/ho práce vč. titulů}▘
%     * \KatedraVedouciho{Název katedry, na které vedoucí práce působí}
%     * \KatedraVedoucihoEN{Název katedry vedoucí/ho v anglickém jazyce}
%     * \StudijniProgram{Studijní program}▖
%     * \StudijniObor{Studjní obor}▖
%     * \Podekovani{Poděkování}▖
%     * \Abstrakt{Abstrakt}
%     * \AbstraktEN{Abstrakt v anglickém jazyce}
%     * \KlicovaSlova{{klíčová} {slova}}
%     * \KlicovaSlovaEN{{klíčová slova} {v} {anglickém jazyce}}
%     * \Konzultant{Jméno konzultanta projektu}▖

\newcommand{\NazevPrace}[1]{\newcommand{\INazevPrace}{#1}}
\newcommand{\NazevPraceEN}[1]{\newcommand{\INazevPraceEN}{#1}}
\newcommand{\AutorPrace}[1]{\newcommand{\IAutorPrace}{#1}}
\newcommand{\RokOdevzdani}[1]{\newcommand{\IRokOdevzdani}{#1}}
\newcommand{\Katedra}[1]{\newcommand{\IKatedra}{#1}}
\newcommand{\KatedraEN}[1]{\newcommand{\IKatedraEN}{#1}}
\newcommand{\TypPracoviste}[1]{\newcommand{\ITypPracoviste}{#1}}
\newcommand{\TypPracovisteEN}[1]{\newcommand{\ITypPracovisteEN}{#1}}
\newcommand{\Vedouci}[1]{\newcommand{\IVedouci}{#1}}
\newcommand{\KatedraVedouciho}[1]{\newcommand{\IKatedraVedouciho}{#1}}
\newcommand{\KatedraVedoucihoEN}[1]{\newcommand{\IKatedraVedoucihoEN}{#1}}
\newcommand{\StudijniProgram}[1]{\newcommand{\IStudijniProgram}{#1}}
\newcommand{\StudijniObor}[1]{\newcommand{\IStudijniObor}{#1}}
\newcommand{\Podekovani}[1]{\newcommand{\IPodekovani}{#1}}
\newcommand{\Abstrakt}[1]{\newcommand{\IAbstrakt}{#1}}
\newcommand{\AbstraktEN}[1]{\newcommand{\IAbstraktEN}{#1}}
\newcommand{\KlicovaSlova}[1]{\newcommand{\IKlicovaSlova}{#1}}
\newcommand{\KlicovaSlovaEN}[1]{\newcommand{\IKlicovaSlovaEN}{#1}}
\newcommand{\Konzultant}[1]{\newcommand{\IKonzultant}{#1}}

\setlength\textwidth{145mm}
\setlength\textheight{247mm}
\setlength\oddsidemargin{15mm}
\setlength\evensidemargin{15mm}
\setlength\topmargin{0mm}
\setlength\headsep{0mm}
\setlength\headheight{0mm}
\let\openright=\clearpage
\DeclareOption{twoside}{
    \PassOptionsToClass{twoside}{report}
    \setlength\textwidth{145mm}
    \setlength\textheight{247mm}
    \setlength\oddsidemargin{14.2mm}
    \setlength\evensidemargin{0mm}
    \setlength\topmargin{0mm}
    \setlength\headsep{0mm}
    \setlength\headheight{0mm}
    \let\openright=\cleardoublepage
}

\def\decl@gender{ }
\DeclareOption{female}{
    \def\decl@gender{a }
}
\def\notes@show{1}
\DeclareOption{final}{
    \def\notes@show{0}
    \PassOptionsToPackage{hidelinks}{hyperref}
}

\def\projtype@title{Bakalářská práce}
\def\projtype@supervisor{bakalářské práce}
\def\projtype@showthesisinfo{1}
\DeclareOption{project}{
    \def\projtype@title{Studentský projekt}
    \def\projtype@supervisor{studentského projektu}
    \def\projtype@showthesisinfo{0}
}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax

\LoadClass[12pt,a4paper]{report}

\RequirePackage[a-2u]{pdfx}
\RequirePackage[czech]{babel}
\RequirePackage{lmodern}
\RequirePackage[T1]{fontenc}
\RequirePackage{textcomp}
\RequirePackage[utf8]{inputenc}
\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{amsthm}
\RequirePackage{bbding}
\RequirePackage{bm}
\RequirePackage{graphicx}
\RequirePackage{fancyvrb}
\RequirePackage{indentfirst}
\RequirePackage{bookmark}
% \RequirePackage{icomma} % FIXME: Missing package
\RequirePackage{dcolumn}
\RequirePackage{booktabs}
\RequirePackage{paralist}
\RequirePackage{xcolor}
\RequirePackage{csquotes}
\RequirePackage{biblatex}
\ifnum\notes@show>0
    \RequirePackage{enumitem,amssymb}
    \newlist{todolist}{itemize}{2}
    \setlist[todolist]{label=$\square$}
    \RequirePackage{pifont}
    \newcommand{\cmark}{\ding{51}}
    \newcommand{\xmark}{\ding{55}}
    \newcommand{\crmark}{\ding{60}}
    \newcommand{\pmark}{\ding{46}}
    \newcommand{\done}{\rlap{$\square$}{\raisebox{2pt}{\large\hspace{1pt}\textcolor{green}{\cmark}}}\hspace{-2.5pt}}
    \newcommand{\wontfix}{\rlap{$\square$}{\large\hspace{1pt}\textcolor{red}{\xmark}}}
    \newcommand{\todo}[1]{{\color{teal}(\textcolor{cyan}{\crmark} #1)}}
    \newcommand{\ask}[1]{{\color{brown}(\textcolor{orange}{\textbf{?}} #1)}}
    \newcommand{\note}[1]{{\color{violet}(\textcolor{magenta}{\pmark} #1)}}
    \overfullrule=1mm
\else
    \RequirePackage{environ}
    \NewEnviron{todolist}{}
    \newcommand{\todo}[1]{}
    \newcommand{\ask}[1]{}
    \newcommand{\note}[1]{}
\fi
\ifnum\projtype@showthesisinfo>0
    \RequirePackage[nottoc]{tocbibind}
\fi

\hypersetup{unicode}
\hypersetup{breaklinks=true}

\renewcommand*{\maketitle}{%
    \begin{titlepage}
        \pagestyle{empty}
        \hypersetup{pageanchor=false}
        \begin{center}

            \centerline{\mbox{\includegraphics[width=166mm]{./img/logo-cs.pdf}}}

            \vspace{-8mm}
            \vfill

            {\bf\Large \MakeUppercase{\projtype@title}}

            \vfill

            {\LARGE\IAutorPrace}

            \vspace{15mm}

            {\LARGE\bfseries\INazevPrace}

            \vfill

            \IKatedra

            \vfill

            {\centerline{\vbox{\halign{
                            \hbox to 0.45\hsize{\hfil ##}&\hskip 0.5em\parbox[t]{0.45\hsize}{\raggedright ##}\cr
                            Vedoucí \projtype@supervisor:&\IVedouci \cr
                            \ifnum\projtype@showthesisinfo<1
                                \ifdefined\IKonzultant
                                    \noalign{\vspace{2mm}}
                                    Konzultant:&\IKonzultant \cr
                                \fi
                            \fi
                            \ifdefined\IStudijniProgram
                                \noalign{\vspace{2mm}}
                                Studijní program:&\IStudijniProgram \cr
                            \fi
                            \ifdefined\IStudijniObor
                                \noalign{\vspace{2mm}}
                                Studijní obor:&\IStudijniObor \cr
                            \fi
                        }}}}

            \vfill

            Praha \IRokOdevzdani
        \end{center}

        \newpage

        \openright

        \pagestyle{plain}
        \hypersetup{pageanchor=true}
        \pagenumbering{roman}

        \ifnum\projtype@showthesisinfo>0
            \vglue 0pt plus 1fill

            \noindent
            Prohlašuji, že jsem tuto bakalářskou práci vypracoval\decl@gender samostatně a výhradně
            s~použitím citovaných pramenů, literatury a dalších odborných zdrojů.
            Tato práce nebyla využita k získání jiného nebo stejného titulu.

            \medskip\noindent
            Beru na~vědomí, že se na moji práci vztahují práva a povinnosti vyplývající
            ze zákona č. 121/2000 Sb., autorského zákona v~platném znění, zejména skutečnost,
            že Univerzita Karlova má právo na~uzavření licenční smlouvy o~užití této
            práce jako školního díla podle §60 odst. 1 autorského zákona.

            \vspace{10mm}

            \hbox{\hbox to 0.5\hsize{%
                    V \hbox to 6em{\dotfill} dne \hbox to 6em{\dotfill}
                    \hss}\hbox to 0.5\hsize{\dotfill\quad}}
            \smallskip
            \hbox{\hbox to 0.5\hsize{}\hbox to 0.5\hsize{\hfil Podpis autora\hfil}}

            \vspace{20mm}
            \newpage

            \openright
        \fi

        \ifdefined\IPodekovani
            \noindent
            \IPodekovani
            \newpage

            \openright
        \fi

        \ifnum\projtype@showthesisinfo>0
            \vbox to 0.5\vsize{
                \setlength\parindent{0mm}
                \setlength\parskip{5mm}

                Název práce:
                \INazevPrace

                Autor:
                \IAutorPrace

                \ITypPracoviste:
                \IKatedra

                Vedoucí bakalářské práce:\\
                \IVedouci, \IKatedraVedouciho

                Abstrakt:\\
                \IAbstrakt

                Klíčová slova:\\
                \IKlicovaSlova

                \vss
            }
            \nobreak\vbox to 0.49\vsize{
                \setlength\parindent{0mm}
                \setlength\parskip{5mm}

                Title:
                \INazevPraceEN

                Author:
                \IAutorPrace

                \ITypPracovisteEN:
                \IKatedraEN

                Supervisor:\\
                \IVedouci, \IKatedraVedoucihoEN

                Abstract:\\
                \IAbstraktEN

                Keywords:\\
                \IKlicovaSlovaEN

                \vss
            }

            \newpage

            \openright
        \fi
    \end{titlepage}


    \pagestyle{plain}
    \pagenumbering{arabic}
    \setcounter{page}{1}
}

\makeatletter
\def\@makechapterhead#1{
  {\parindent \z@ \raggedright \normalfont
   \Huge\bfseries \thechapter. #1
   \par\nobreak
   \vskip 20\p@
}}
\def\@makeschapterhead#1{
  {\parindent \z@ \raggedright \normalfont
   \Huge\bfseries #1
   \par\nobreak
   \vskip 20\p@
}}
\makeatother

\def\chapwithtoc#1{
\chapter*{#1}
\addcontentsline{toc}{chapter}{#1}
}

% Trochu volnější nastavení dělení slov, než je default.
\lefthyphenmin=2
\righthyphenmin=2

%%% Makra pro definice, věty, tvrzení, příklady, ... (vyžaduje baliček amsthm)

\theoremstyle{plain}
\newtheorem{veta}{Věta}
\newtheorem{lemma}[veta]{Lemma}
\newtheorem{tvrz}[veta]{Tvrzení}

\theoremstyle{plain}
\newtheorem{definice}{Definice}

\theoremstyle{remark}
\newtheorem*{dusl}{Důsledek}
\newtheorem*{pozn}{Poznámka}
\newtheorem*{prikl}{Příklad}

%%% Prostředí pro důkazy

\newenvironment{dukaz}{
  \par\medskip\noindent
  \textit{Důkaz}.
}{
\newline
\rightline{$\qedsymbol$}
}

%%% Prostředí pro sazbu kódu, případně vstupu/výstupu počítačových
%%% programů. (Vyžaduje balíček fancyvrb -- fancy verbatim.)

\DefineVerbatimEnvironment{code}{Verbatim}{fontsize=\small, frame=single}

%%% Prostor reálných, resp. přirozených čísel
\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}

%%% Užitečné operátory pro statistiku a pravděpodobnost
\DeclareMathOperator{\pr}{\textsf{P}}
\DeclareMathOperator{\E}{\textsf{E}\,}
\DeclareMathOperator{\var}{\textrm{var}}
\DeclareMathOperator{\sd}{\textrm{sd}}

%%% Příkaz pro transpozici vektoru/matice
\newcommand{\T}[1]{#1^\top}

%%% Vychytávky pro matematiku
\newcommand{\goto}{\rightarrow}
\newcommand{\gotop}{\stackrel{P}{\longrightarrow}}
\newcommand{\maon}[1]{o(n^{#1})}
\newcommand{\abs}[1]{\left|{#1}\right|}
\newcommand{\dint}{\int_0^\tau\!\!\int_0^\tau}
\newcommand{\isqr}[1]{\frac{1}{\sqrt{#1}}}

%%% Vychytávky pro tabulky
\newcommand{\pulrad}[1]{\raisebox{1.5ex}[0pt]{#1}}
\newcommand{\mc}[1]{\multicolumn{1}{c}{#1}}