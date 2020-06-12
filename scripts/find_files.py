"""
A script to list files, pulled from: https://developers.google.com/drive/api/v3/reference/files/list
"""
params = CLI.get_parse_dict(
    (
        "--corpora",
        dict(
            default="", type=str, dest='corpora',
            help="Bodies of items (files/documents) to which the query applies. Supported bodies are 'user', 'domain', 'drive' and 'allDrives'. Prefer 'user' or 'drive' to 'allDrives' for efficiency.'"
        )
    ),
    (
        "--driveId",
        dict(
            default="", type=str, dest='driveId',
            help='ID of the shared drive to search'
        )
    ),
    (
        '--fields',
        dict(
            default="files(id,name)", type=str, dest='fields',
            help="The paths of the fields you want included in the response. If not specified, the response includes a default set of fields specific to this method. For development you can use the special value * to return all fields, but you'll achieve greater performance by only selecting the fields you need. For more information see the partial responses documentation."
        )
    ),
    (
        '--orderBy',
        dict(
            default="", type=str, dest='orderBy',
            help="A comma-separated list of sort keys. Valid keys are 'createdTime', 'folder', 'modifiedByMeTime', 'modifiedTime', 'name', 'name_natural', 'quotaBytesUsed', 'recency', 'sharedWithMeTime', 'starred', and 'viewedByMeTime'. Each key sorts ascending by default, but may be reversed with the 'desc' modifier. Example usage: ?orderBy=folder,modifiedTime desc,name. Please note that there is a current limitation for users with approximately one million files in which the requested sort order is ignored."
        )
    ),
    (
        '--pageSize',
        dict(
            default=25, type=int, dest='pageSize',
            help="The maximum number of files to return per page. Partial or empty result pages are possible even before the end of the files list has been reached. Acceptable values are 1 to 1000, inclusive. (Default: 100"
        )
    ),
    (
        '--pageToken',
        dict(
            default="", type=str, dest='pageToken',
            help="The token for continuing a previous list request on the next page. This should be set to the value of 'nextPageToken' from the previous response"
        )
    ),
    (
        '--q',
        dict(
            default="", type=str, dest='q',
            help="A query for filtering the file results. 'See the Search for files' guide for the supported syntax."
        )
    ),
    (
        '--spaces',
        dict(
            default="", type=str, dest='spaces',
            help="A comma-separated list of spaces to query within the corpus. Supported values are 'drive', 'appDataFolder' and 'photos'."
        )
    ),
    (
        '--supportsAllDrives',
        dict(
            default=True, action='store_const', const=True, dest='supportsAllDrives',
            help="Deprecated - Whether the requesting application supports both My Drives and shared drives. This parameter will only be effective until June 1, 2020. Afterwards all applications are assumed to support shared drives."
        )
    ),
    (
        '--includeItemsFromAllDrives',
        dict(
            default=True, action='store_const', const=True, dest='includeItemsFromAllDrives',
            help="Deprecated - Whether to include files from all drives"
        )
    )
)
files_api = Files() #

file_listing = files_api.list(**params)

print("\n".join(str(f) for f in file_listing))