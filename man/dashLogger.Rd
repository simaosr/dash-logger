% Auto-generated: do not edit by hand
\name{dashLogger}

\alias{dashLogger}

\title{DashLogger component}

\description{
DashLogger component for displaying logs in real-time.
}

\usage{
dashLogger(id=NULL, className=NULL, loggerName=NULL, loggerNames=NULL,
maxLogs=NULL, style=NULL, timestampFormat=NULL,
twoColumns=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{className}{Character. Additional class name for the logger container}

\item{loggerName}{Character. Name of the logger to display (for single logger view)}

\item{loggerNames}{List of characters. Names of loggers to display (for combined view)}

\item{maxLogs}{Numeric. Maximum number of logs to display}

\item{style}{Named list. Additional inline styles for the logger container}

\item{timestampFormat}{Character. The format string for the timestamp}

\item{twoColumns}{Logical. Whether to display logs in two columns (timestamp and message)}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

