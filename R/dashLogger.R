# AUTO GENERATED FILE - DO NOT EDIT

#' @export
dashLogger <- function(id=NULL, className=NULL, loggerName=NULL, loggerNames=NULL, maxLogs=NULL, style=NULL, timestampFormat=NULL, twoColumns=NULL) {
    
    props <- list(id=id, className=className, loggerName=loggerName, loggerNames=loggerNames, maxLogs=maxLogs, style=style, timestampFormat=timestampFormat, twoColumns=twoColumns)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DashLogger',
        namespace = 'dash_logger',
        propNames = c('id', 'className', 'loggerName', 'loggerNames', 'maxLogs', 'style', 'timestampFormat', 'twoColumns'),
        package = 'dashLogger'
        )

    structure(component, class = c('dash_component', 'list'))
}
