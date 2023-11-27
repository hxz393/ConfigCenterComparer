# [English](https://github.com/hxz393/ConfigCenterComparer/blob/main/doc/README_EN.md) | [中文](https://github.com/hxz393/ConfigCenterComparer/blob/main/README.md)

# Introduction

`ConfigCenterComparer` is a configuration center comparison tool. Its primary function is to compare configuration data across different configuration centers, ensuring consistency and accuracy of configurations between environments.

Key Features:

- **Support for Multiple Configuration Centers**: Compatible with mainstream configuration centers such as `Apollo` and `Nacos`, allowing for cross-cluster data retrieval.
- **Data Formatting and Comparison**: Provides a graphical user interface for easy data formatting and comparison.
- **Database Integration**: Integrates with MySQL database querying module, supporting SSH tunnel connections.
- **Log Recording and Error Handling**: Equipped with an advanced logging system and error handling mechanisms.
- **Practical Utilities**: Includes various features like search, copy, export, and more.

Screenshot:

![main screen](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/main_screen_en.jpg)

## Usage Requirements

The following usage scenarios are described for your reference. Unless explicitly stated as unsupported, results should be tested independently.

### Operating Systems

- **Development Environment**: `Windows 10 Professional Workstation Edition`, version `22H2`.
- **Compatibility**: Supports `Win 7 x64` and higher versions of operating systems. Does not support `Win XP`. Also compatible with `Windows Server 2008` and above.
- **Cross-Platform Features**: Due to QT's cross-platform characteristics, it's theoretically possible to manually compile executables for other operating systems. See the following sections for compilation guidelines.

### Configuration Centers

Nacos supports configurations in `yaml` format. Other formats are not supported.

Tested configuration centers and their versions:

- **Apollo**: `2.0.x`, `2.1.x`
- **Nacos**: `v2.1.x`

Other versions have not been tested. Differences in database structure may lead to query failures. Feedback on related issues is welcome.

### Database

- **Tested Version**: MySQL `5.7`. In theory, `8.x` should also be supported.
- **Case Sensitivity**: Database configurations should disable case sensitivity. Apollo's database query SQL uses camel case and disregards case sensitivity settings. The compatibility of Nacos' database configuration remains to be verified, and feedback is welcome.



## Getting the Program

On the Windows platform, two versions have been packaged. For Windows 7, the compatible version is marked with `-Win7(x64)` in the file name, which can be downloaded as needed. Users of other operating systems can try building the executable from the source code or run it in a Python IDE.

### Download Links

Ways to download the software:

- **Method 1**: Visit the [release](https://github.com/hxz393/ConfigCenterComparer/releases) page to download `ConfigCenterComparer.exe`.
- **Method 2**: [Direct link](https://www.x2b.net/download/ConfigCenterComparer.7z) download.

The downloaded compressed file needs to be extracted before running; otherwise, the program's configuration will have nowhere to be saved.

### Manual Packaging

Manual compilation requires prior installation of `Python 3.7` or higher, `PyQT 5.10` or higher, and the `pyinstaller 5.6` package. Other third-party dependencies include `PyMySQL`, `PyYAML`, `paramiko`, `requests`, `sshtunnel`, with no specific version requirements.

The compilation steps are as follows:

1. Clone the project on a system with `Git` installed. Use the command:

   ```sh
   git clone https://github.com/hxz393/ConfigCenterComparer.git
   ```

   Alternatively, click the green `<> Code` button on the [project homepage](https://github.com/hxz393/ConfigCenterComparer) and select the `Download ZIP` option to [download](https://github.com/hxz393/ConfigCenterComparer/archive/refs/heads/main.zip) the source code zip file. After downloading, extract the contents using a compression tool or command.

2. Switch to the project path using a command.

   For example, in Windows, open the `CMD` prompt and enter:

   ```sh
   cd B:\git\ConfigCenterComparer
   B:
   ```

   In Linux, use the `cd` command to navigate to the project path:

   ```sh
   cd /root/ConfigCenterComparer
   ```

   If using `PyCharm` as an IDE, you can directly enter the packaging command in the built-in terminal.

3. Use the `pyinstaller` command to compile and package into an executable file:

   ```sh
   pyinstaller -F -w -i media/main.ico --add-data 'media/;media' ConfigCenterComparer.py
   ```

   If using `Anaconda` as a virtual environment, add the `-p` parameter when packaging to specify the directory of the virtual environment. For example:

   ```sh
   pyinstaller -F -w -i media/main.ico --add-data media/;media -p C:\ProgramData\Anaconda3\envs\ccc ConfigCenterComparer.py
   ```

   After successful compilation, the executable file will be generated in the `dist` directory.



## Development Related

Below is information related to the development of the program.

### Program Principles

The main workflow of the program is as follows:

1. By querying Apollo's database tables `app`, `namespace`, and `item`, it retrieves data for fields `AppId` (or `Name`), `NamespaceName`, `Key`, `Value`, and `DataChange_LastTime`.

   For Nacos databases, it queries the `config_info` table for fields `data_id`, `group_id`, `content`, and `gmt_modified`. Then, it parses and splits the `yaml` format content in the `content` field into multiple configuration entries.

2. For each configuration entry, it combines the name, group, and key name as a unique index and merges the configuration values and modification times from different environments into the result dictionary.

3. It compares the values across different configuration environments to determine consistency and updates this information in the result dictionary.

4. The program checks against a filter list to determine if certain entries should be filtered out and updates this information in the result dictionary.

5. All results are inserted into the main window table.

6. Filters are applied to color-code table rows or cells and perform other display optimization actions.

If an error occurs during the program's operation, as long as it doesn't affect the functioning, no popup message will appear. However, an "Error Occurred" notice will be displayed in the status bar label at the bottom right. You can check the logs for potential program bugs or other issues.

### Module Descriptions

The project structure is outlined as follows:

- `ConfigCenterComparer.py`: The main program.
- `config/`: Configuration folder, containing language dictionaries and global variables.
- `lib/`: A utility library storing common functions, including file handling, database queries, etc.
- `media/`: Media folder, storing icons and other media files.
- `module/`: Contains modules related to project-specific functions, such as querying configuration paths, executing queries, and formatting results.
- `ui/`: Modules related to UI definition and operations.

### Language Translation

Given the minimal amount of program text, a language dictionary is used to store all display texts. The file path is: `config\lang_dict_all.py`. Additional language translations can be added in this file.

### Open Source License

This project adheres to the [GPL-3.0 license](https://github.com/hxz393/ConfigCenterComparer/blob/main/LICENSE). Violations of the open-source community guidelines will result in legal action.



# Usage

Before using `ConfigCenterComparer`, please read this section carefully.

## Settings

Initial configuration is required upon first use.

### Program Settings

In the toolbar or under the 'Options' menu, select 'Program Settings' to enter the settings interface, as shown in the following image:

![main settings](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/main_settings_en.jpg)

The configuration file is located at `config\config_main.json`. Do not modify it manually to avoid errors. If the configuration file is corrupted, it can be deleted and regenerated.

Descriptions of various configuration items are as follows:

- **Select Language**

  The default is 'English'. Select to switch the display language of the program.

- **Select Configuration Center Type**

  Options include 'Apollo' or 'Nacos'. Based on the selection, the program reads different connection configuration files.

- **Select Apollo Service Name Field**

  Effective when the configuration center type is set to 'Apollo'. It sets which database field is displayed as the service name. Dropdown options 'AppId' and 'Name' correspond to 'AppId' and 'Application Name' in Apollo's 'Application Information'.

- **Table Color Switch**

  If there are tens of thousands of configuration entries, you can turn off the table color display to significantly improve running speed.

- **Replace Service Name**

  - Enter 'Original Name' and 'New Name' in the input box to fully replace the service name. This is commonly used for aligning service names in different environments. For instance, if the AppId in the development environment is '1025', and in other environments, it's named 'api-web', replacing 1025 with api-web allows for the comparison of configurations for 'api-web' in the program.
  - Multiple sets of service name replacements can be configured, with each set separated by a space. The number of fields in 'Original Name' and 'New Name' must match, and the contents must correspond; otherwise, the excess fields will be truncated. Each service name undergoes replacement only once.
  - Replacement occurs only when there's an exact match of the service name. In the above example, 1025 will not match service names like '10258' or 'api-1025'. Full names are required for replacements.
  - Service name replacement is carried out after trimming service names, so be aware of the sequence.

- **Trim Service Name**

  - Removes prefixes or suffixes from the service name. Similar to replacing service names, this is used for aligning service names. The prefix is matched from the start of the service name, and the suffix from the end. If matched, the corresponding text is deleted from the service name. For example, if the suffix to be trimmed is '.yaml', then service names like 'api-web.yaml' will be replaced with 'api-web'.
  - Multiple sets of trimming fields can be configured, with each set separated by space. Each service name undergoes prefix and suffix trimming only once; if a match is found, subsequent checks are not performed. For example, if the prefix to be trimmed is 'pc-' and the suffix is '.yaml -web', then the service name 'pc-api-web.yaml' can be trimmed to a maximum of 'api-web'.
  - Both service name trimming and replacement are case-sensitive.

### Connection Settings

After configuring the main settings, it is necessary to set up the database. From the toolbar or the "Options" menu, click on the "Connection Settings" button or option to enter the database configuration window, as shown in the image:

![connect settings](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/connect_settings_en.jpg)



The connection settings for Apollo and Nacos are separately stored in `config\config_apollo.json` and `config\config_nacos.json`. It is advised not to modify these manually.

Up to four sets of environment configurations can be compared, which can be switched between using tabs. The configuration requirements for connecting to Apollo and Nacos are the same, and the details of each configuration item are as follows:

- **Enable**

  By checking the "Enable" option in the "MySQL Connection Configuration", the current environment is included in the configuration comparison. If you need to connect to the database via an SSH tunnel, check the "Enable" option in the "SSH Tunnel Configuration" and enter the relevant parameters.

- **Address**

  Enter the IP address or domain name of the MySQL or SSH host. For example: "192.168.1.1" or "yourdomain.com".

- **Port**

  Enter the port number for the MySQL or SSH connection. For example: "3306" or "22".

- **Username**

  Enter the username that has connection permissions. For example: "apollo" or "root".

- **Password**

  Enter the password for the connection username.

- **Database**

  Specify the name of the database where the configuration is stored. For example, the default database name used by Apollo is "ApolloConfigDB", and for Nacos, it is "nacos".



## Getting Started

After clicking the "Test" or "Run" buttons, they will turn grey. A pop-up window or data will be displayed upon completion of the operation. The completion time mainly depends on the network speed, so please be patient.

### Testing

After configuring the database connection, you can perform a connectivity test. From the toolbar or the "Start" menu, click on the "Test" button or option to start the test:

- If the connection is smooth, a pop-up window displaying the MySQL and SSH connection test results will appear in about 10 seconds.
- If there are network or configuration issues causing the connection to fail, it may take some time before the test results are displayed in a pop-up window. The specific reasons for the connection failure can be analyzed in the "View Logs" section.

### Running

Once all configurations are complete, click the "Run" button or option from the toolbar or "Start" menu to begin retrieving data from the database:

- If everything goes well, the main window form will display all the data pulled from the database.
- If the connection fails in some environments, the corresponding environment configurations will not be displayed in the final results. The specific reasons for the connection failure can be analyzed in the "View Logs" section.
- To retrieve updated configurations, you can click "Run" again to refresh the table. The program does not cache the results to local files.

### Compare

After retrieving data from the database, you can perform a further duplication check by clicking on the "Compare" button or option from the toolbar or "Start" menu. This feature compares duplicate configurations within the same environment. For example:

If the database connection pool size is configured in the public namespace, and the same setting with the same value is configured in the private namespace of another application, it can be considered a duplicate configuration in the private settings.

The compare feature can identify such configurations. The results window for the duplication check is shown in the following image:

![connect settings](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/comparison_results_en.jpg)

The window is divided into two parts:

- The main area is the duplication check results table, differentiated by tabs for different environments. Besides the fields seen in the main window, there is a column of numbers on the far left, consisting of group numbers and internal group numbers.
- Above are two input boxes, whose specific functions are:
  - Public Namespace Input Box, for marking the line where the public configuration is located. For example, entering `global` and clicking "Set" will display the entire line where `global` is located in red font.
  - Search Configuration Input Box, for searching content within configuration keys or values. Rows with no matching content will be hidden. The search field is case-insensitive.



## Result Display

The main interface is divided from top to bottom into the menu bar, toolbar, filter bar, main table, and status bar. The focus here is on the main table.

### Table Header

The table header consists of the following items:

- **Name**: This refers to the service name. In Apollo, it is known as "AppId" or "Application Name". In Nacos, it is represented by a single field called "Data Id".
- **Group**: In Apollo, this is the "Namespace", usually the private namespace is called "application". In Nacos, the equivalent field is "Group".
- **Key**: In Apollo, this is referred to as "Key". In Nacos, it is extracted from "Configuration Content" and follows the same format as in Apollo.
- **Value**: By default, this is divided into four columns for different environments, with the headers being the names of the environments. In Apollo, it is "Value". In Nacos, it is extracted from "Configuration Content".
- **Modified Time**: This is hidden by default. It is divided into four columns for different environments, representing the last modification time of the corresponding environment configuration.
- **Consistency**: This is divided into four statuses.
  - Fully Consistent: Indicates that all environment configuration values are exactly the same. Requires at least two environments for comparison.
  - Partially Consistent: The values in the production environment and the preview environment are equal, but different from other environments.
  - Unknown Status: Only a single environment has a value. Other environments may not have a configuration or the value retrieval may have failed.
  - Inconsistent: All situations that do not meet the above statuses are considered inconsistent.
- **Skip**: The value can be either "Yes" or "No". This is set manually by the user.

The table header supports drag-and-drop arrangement, and clicking on the header can sort the table. The right-click context menu on the header allows you to hide or show certain columns.

### Colors

Once the configuration data is retrieved, the main window form displays each configuration status in different colors, which signify the following:

- Grey: Included in the skip list, where the skip value is "Yes".
- Green: The consistency value is "Fully Consistent".
- Blue: The consistency value is "Partially Consistent".
- Red: Cells that either have no configuration or failed to retrieve the configuration value.
- White: The default state.



## Filter Operations

The filter bar is divided into three parts: filter service, quick filter, and global search. These methods can be combined to quickly find and compare configurations.

### Filter Name

Select a service name from the dropdown box, and the table will display only the configurations of the selected service. By default, all configurations are displayed.

### Quick Filter

This applies to the "Consistency" and "Skip" columns. Select a filtering condition from the dropdown box. If the selected condition matches the value of a row, that row will be hidden from the table.

If the "Invert" box is checked, then only the rows matching the selected condition will be displayed in the table.

### Global Search

Enter the search content in the input box and click the search button to perform a string search across all table data. Cells with matching values will be highlighted, and rows without matching values will be hidden.

### Reset Conditions

By clicking the reset button next to the search button, all filter conditions will be reset, clearing the content in the search input box, and the full table content will be displayed.



## Editing Operations

The program does not modify any original configurations. The skip list is stored in the local file `config\config_skip.txt`.

### Copy Content

Click or drag a cell with the mouse, then select "Copy" from the right-click context menu or the toolbar. The selected data will be copied to the system clipboard.

### Export List

Export the data displayed in the current table to a file. From the "Edit" menu bar or the right-click context menu on the table, select "Export". In the file save window, choose the export format. It supports `JSON` or `CSV` formats. Click save to export the data.

### Ignore Operation

Users can customize which configuration rows to ignore. Click or drag a cell with the mouse, then select "Skip" from the right-click context menu or the toolbar. The configuration row will be marked as ignored. Afterwards, quick filter can be applied to hide the ignored configuration rows.

To undo the ignore operation, select "Unskip", and the configuration row will be removed from the filter list.



## Help Operations

This includes viewing logs, checking for new versions of the program, and viewing program information.

### View Logs

Select "View Logs" from the "Help" menu or quick toolbar to open the log viewing window:

![view logs](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/view_logs_en.jpg)

In the top-left dropdown box, you can select the log level you wish to display. For example, if you choose "WARNING", only logs of WARNING level and above will be displayed, and INFO level logs will be filtered out.

The "Feedback" button in the bottom left corner, when clicked, will redirect to the GitHub project's Issues page, making it easy to submit error reports.

The "Clear" button in the bottom left corner, when clicked, will clear the contents of the log file. Log files are stored in the `logs` directory. If a file exceeds 1MB, it will roll over, with a maximum of ten files being retained.

The "Refresh" button in the bottom right corner can be clicked to switch the log display to continuous mode, which is convenient for monitoring logs.

### Check for Updates

Select "Check Updates" from the "Help" menu to check online if there is an updated version of the program available. The result of the check will be notified via a pop-up window.

### About Program

Select "About" from the "Help" menu to display a pop-up with program explanations and build information.

### Debugging the Program

This is used for development and debugging code and is not of practical use to users.



# FAQ

When encountering errors during software operation, first check the logs. If the issue is related to connectivity, please verify your configurations and try again. Then, refer to the solutions for common problems listed below. Lastly, check all [Issues](https://github.com/hxz393/ConfigCenterComparer/issues) to see if the same problem exists. If further help is needed, submit a new Issue and attach the relevant logs.



# Update Log

To avoid an excessively long update log, only the most recent updates are retained.

## Version 1.1.0 (2023.11.28)

New Features:

1. Added configuration duplication check feature;
2. Refresh button added to the log viewing window.

Enhancements:

1. Modified the language management class for immediate effect upon language switch, eliminating the need to restart;
2. Changed configuration management class to reduce the number of reads from the configuration file;
3. Updated the log viewing window display mode to operate independently of the main window;
4. Adjusted the code to support down to Python 3.7 and provided a version compatible with Windows 7.



## Version 1.0.2 (2023.11.21)

New Features:

1. Added a table color switch to address performance issues due to large data volumes.

Fixes:

1. Modified color application logic to improve performance;
2. Optimized main thread code to enhance UI stability.



## Version 1.0.1 (2023.11.19)

Fixes:

1. Cleared filter bar conditions before starting to run, preventing interface freezing on subsequent runs;
2. Improved log display text.



## Version 1.0.0 (2023.11.19)

First release.

