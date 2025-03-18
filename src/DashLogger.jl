
module DashLogger
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "0.0.1"

include("jl/dashlogger.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "dash_logger",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "dash_logger.min.js",
    external_url = nothing,
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "dash_logger.min.js.map",
    external_url = nothing,
    dynamic = true,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "assets/dash_logger.css",
    external_url = "https://unpkg.com/dash_logger@0.0.1/dash_logger/assets/dash_logger.css",
    dynamic = nothing,
    async = nothing,
    type = :css
)
            ]
        )

    )
end
end
