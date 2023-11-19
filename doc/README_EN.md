# [English](https://github.com/hxz393/ConfigCenterComparer/blob/main/doc/README_EN.md) | [中文](https://github.com/hxz393/ConfigCenterComparer/blob/main/README.md)

# Program Introduction

`ConfigCenterComparer` is a configuration center comparison tool. Its primary function is to compare configuration data across different configuration centers, ensuring consistency and accuracy of configurations across environments.

Main Features:

- **Supports Multiple Configuration Centers**: Compatible with mainstream `Apollo` and `Nacos` configuration centers. Implements cross-cluster data retrieval.
- **Data Formatting and Comparison**: Provides a graphical interface for convenient data formatting and comparison.
- **Database Integration**: Integrates MySQL database query module, supporting SSH tunnel connections.
- **Log Recording and Error Handling**: Equipped with an advanced log system and error handling mechanism.
- **Practical Functions**: Includes various features such as search, copy, export, and an skip list.

![main screen](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/main_screen_en.jpg)

## Requirements

The following use case descriptions apply, unless explicitly stated as unsupported, and results should be tested independently.

### Operating Systems

- **Development Environment**: `Windows 10 Professional Workstation Edition`, version `22H2`.
- **Compatibility**: Supports `Win10 x64` and higher versions of the operating system. Does not support `Win 7` and `Win XP`, due to the use of `Python 3.10`.
- **Cross-Platform Features**: Thanks to QT's cross-platform characteristics, it is theoretically possible to manually compile the software into executable files for other operating systems. Compilation guide is detailed below.

### Configuration Centers

Nacos supports configurations in `yaml` format. Other formats are not supported.

Tested configuration centers and versions:

- **Apollo**: `2.0.x`, `2.1.x`
- **Nacos**: `v2.1.x`

Other versions have not been tested. Database structure differences may lead to query failures. Feedback on related issues is welcome.

### Database

- **Tested Version**: MySQL `5.7`. Theoretically, `8.x` should also be supported.
- **Case Sensitivity**: The database configuration should be set to case-insensitive. Apollo's database query SQL uses camel case and ignores case sensitivity settings. Compatibility with Nacos database configuration is pending verification, and feedback is welcome.



## Getting the Program

For users of Win10 and above, the program can be directly downloaded and used. Users of other operating systems can try to build an executable from the source code, or run it in a Python IDE.

### Download Address

Methods to download the software:

- **Method 1**: Go to the [release](https://github.com/hxz393/ConfigCenterComparer/releases) page and download `ConfigCenterComparer.exe`.
- **Method 2**: [Direct link](https://www.x2b.net/download/ConfigCenterComparer.7z) download.

The downloaded compressed file needs to be extracted before running the executable file, otherwise, the program configuration will not be saved.

### Manual Packaging

Manual compilation requires prior installation of `Python 3.10` or above, `PyQT 5.15` or above, and the `pyinstaller` package. Install other dependencies as they are reported missing.

Compilation steps are as follows:

1. Clone the project on a system with `Git` installed. Use the following command:

   ```sh
   git clone https://github.com/hxz393/ConfigCenterComparer.git
   ```

   Or, on the [project homepage](https://github.com/hxz393/ConfigCenterComparer), click the green `<> Code` button and choose the `Download ZIP` option to [download](https://github.com/hxz393/ConfigCenterComparer/archive/refs/heads/main.zip) the source code zip file. After downloading, use compression software or command tools to extract it.

2. Use the command to switch to the project path.

   For example, in Windows, open the `CMD` command prompt and enter:

   ```sh
   cd B:\git\ConfigCenterComparer
   B:
   ```

   In Linux, use the `cd` command to switch to the project path:

   ```sh
   cd /root/ConfigCenterComparer
   ```

   If using `PyCharm` as an IDE, you can directly enter the following packaging command in the built-in terminal.

3. Use the `pyinstaller` command to compile and package into an executable file:

   ```sh
   pyinstaller -F -w -i media/main.ico --add-data 'media/;media' ConfigCenterComparer.py
   ```

   After successful compilation, the executable file will be generated in the `dist` directory.



## Development Related

Below is information related to development.

### Program Principles

The main workflow of this program is as follows:

1. By querying Apollo's database `app`, `namespace`, and `item` tables, it retrieves data for fields `AppId` (or `Name`), `NamespaceName`, `Key`, `Value`, and `DataChange_LastTime`. 
   For the Nacos database, it queries the `config_info` table for fields `data_id`, `group_id`, `content`, and `gmt_modified`. Then, it parses the `yaml` formatted content in the `content` field into multiple configurations.
2. For each configuration, it combines the name, group, and key as a unique index and merges the configuration values and modification times from different environments into the result dictionary.
3. It compares the values of different configuration environments, obtains consistency information, and updates the result dictionary.
4. By comparing against a filter list, it determines whether to filter and updates the result dictionary.
5. Inserts all results into the main window table.
6. Applies filters to color table rows or cells and performs other display optimization actions.

If an error occurs during program execution, as long as it does not affect the operation, there will be no popup notifications, but an "Error occurred" message will be displayed in the status bar label at the bottom right. Logs can be checked for program bugs or other issues.

### Module Description

The project structure is as follows:

- `ConfigCenterComparer.py`: The main program.
- `config/`: Configuration folder, containing language dictionaries and global variables.
- `lib/`: Utility library, containing general functions such as file handling, database querying, etc.
- `media/`: Media folder, storing icons, etc.
- `module/`: Contains modules related to project functions, such as querying configuration paths, executing queries, and formatting results.
- `ui/`: Modules related to UI definition and operations.

### Language Translation

Due to the small amount of program text, a language dictionary is used to store all display texts. The file path is: `config\lang_dict_all.py`, where other language translations can be added.

### Open Source License

Follows the [GPL-3.0 license](https://github.com/hxz393/ConfigCenterComparer/blob/main/LICENSE). Violations of the open source community guidelines will be subject to legal action.



# Program Usage

Before using `ConfigCenterComparer`, please read this section carefully.

## Settings

On first use, you need to enter the settings page for configuration.

### Program Settings

In the toolbar or the "Options" menu, select "Program Settings" to enter the settings interface, as shown in the image below:

![main settings](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/main_settings_en.jpg)

The configuration file is located at `config\config_main.json`. Do not modify it manually to avoid errors. If the configuration file is corrupted, it can be deleted and regenerated.

The explanations for each configuration item are as follows:

- **Select Language**

  Default is "English". The program needs to be restarted after changing the language.

- **Select Configuration Center Type**

  Choose between "Apollo" or "Nacos". Reads different connection configuration files based on the selection.

- **Select Apollo Service Name Field**

  Effective when the configuration center type is set to "Apollo". It sets which database field to use as the service name display field. Dropdown options "AppId" and "Name" correspond to the "AppId" and "Application Name" in Apollo's "Application Information".

- **Table Color Switch**

  If the number of configuration entries exceeds ten thousand, you can turn off the display of table colors to significantly improve execution speed.

- **Replace Service Name**

  - Enter the "original name" and "new name" in the input box to completely replace the service name. This is usually used for aligning service names across different environments. For example, if the AppId in the development environment is "1025" and the AppId in other environments is "api-web", replacing 1025 with api-web allows for comparing configurations of api-web in the program.
  - Multiple sets of service name replacements can be set, separated by spaces. The number of fields in the "original name" and "new name" must be the same, and their content must correspond; otherwise, excess fields will be truncated. Replacement operation is performed only once for each service name.
  - Replacement occurs only if there is an exact match of the service name. In the example above, 1025 will not match service names like "10258" or "api-1025". Full names must be entered for replacement.
  - Service name replacement is performed after trimming the service name. Please pay attention to the order.

- **Trim Service Name**

  - Removes prefixes or suffixes from the service name. Similar to replacing the service name, it is used for aligning service names. Prefixes match from the beginning of the service name, and suffixes match from the end of the service name. If matched, the matched text is removed from the service name. For example, if the suffix trim is set to ".yaml", then all service names like "api-web.yaml" will be replaced with "api-web".
  - Multiple sets of trimming fields can be set, separated by spaces. Each service name undergoes prefix and suffix trimming only once; if matched, no further checks are conducted. For example, if the prefix trim is set to "pc-" and the suffix trim is set to ".yaml -web", then the service name "pc-api-web.yaml" can be trimmed at most to "api-web".
  - Both service name trimming and replacement operations are case-sensitive.

### Connection Settings

After configuring the main settings, you also need to configure the database. From the toolbar or "Options" menu, click the "Connection Settings" button or option to enter the database configuration window, as shown in the image below:

![connect settings](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/connect_settings_en.jpg)

The connection configurations for Apollo and Nacos are saved in `config\config_apollo.json` and `config\config_nacos.json`, respectively. Again, it is not recommended to modify these files manually.

Up to four sets of environment configurations can be compared, switchable through tabs. The required configurations for Apollo and Nacos connections are the same, and each configuration item is explained as follows:

- **Enable**

  Only after checking the "Enable" option in the "MySQL Connection Configuration" will the current environment be included in the configuration comparison. If you need to connect to the database through an SSH tunnel, check the "Enable" option in the "SSH Tunnel Configuration" and fill in the relevant parameters.

- **Address**

  Enter the IP address or domain name of the MySQL or SSH host. For example: "192.168.1.1" or "yourdomain.com".

- **Port**

  Enter the port number for the MySQL or SSH connection. For example: "3306" or "22".

- **Username**

  Enter a username with connection permissions. For example: "apollo" or "root".

- **Password**

  Enter the password for the connection username.

- **Database**

  Specify the name of the database where the configuration is stored. For example, the default database name used by Apollo is "ApolloConfigDB", and for Nacos, it is "nacos".



## Starting

After clicking the "Test" or "Run" button, the button becomes greyed out. A popup or data will display once the operation is complete. The completion time depends on the network speed, so please be patient.

### Testing

After configuring the database connection, you can perform a connectivity test first. From the toolbar or the "Start" menu, click the "Test" button or option to conduct the test:

- If the connection is smooth, a popup indicating a successful test result will appear after about 10 seconds.
- If there are network or configuration issues causing a connection failure, it may take some time before a popup displays the test result. You can analyze the specific reasons for the connection failure in "View Logs".

### Running

Once all configurations are complete, from the toolbar or the "Start" menu, click the "Run" button or option to start retrieving data from the database:

- If everything goes well, the main window form will display all the data retrieved from the database.
- If the connection fails in some environments, the configurations for those environments will not be displayed in the final results. You can analyze the specific reasons for the connection failure in "View Logs".
- To retrieve updated configurations, you can click "Run" again to refresh the table. The program does not cache results to a local file.



## Result Display

The main interface includes a menu bar, toolbar, filter bar, main table, and status bar. The main table is described in detail below.

### Table Header

The table header is divided into the following items:

- **Name**: The service name, in Apollo it's "AppId" or "Application Name". In Nacos, there is only one field, "Data Id".
- **Group**: In Apollo, it's the "Namespace", usually the private namespace is called "application". In Nacos, the field is "Group".
- **Key**: In Apollo, it's "Key". In Nacos, it's extracted from "Configuration Content", formatted the same as in Apollo.
- **Value**: By default, divided into four columns for different environments, with the environment names as headers. In Apollo, it's "Value". In Nacos, it's extracted from "Configuration Content".
- **Modified Time**: By default hidden. Divided into four columns for different environments, indicating the last modification time of the configuration in the corresponding environment.
- **Consistency**: Divided into four statuses.
  - Fully Consistent: Indicates that all environment configuration values are exactly the same. Requires at least two comparison environments.
  - Partially Consistent: The production environment and preview environment values are equal, but differ from values in other environments.
  - Unknown Status: Only a single environment has a configuration value. Other environments may not have a configuration, or the value retrieval may have failed.
  - Inconsistent: All cases that do not fit the above statuses are classified as inconsistent.
- **Skip**: The value is either "Yes" or "No". Set manually by the user.

The table header supports drag-and-drop arrangement, and clicking on the header can sort the table. Right-clicking on the header allows you to choose to hide or show certain columns.

### Colors

After retrieving the configuration data, the main window form will display each configuration status in different colors. Their meanings are as follows:

- Gray: In the skip list, with the skip value set to "Yes".
- Green: Consistency value is "Fully Consistent".
- Blue: Consistency value is "Partially Consistent".
- Red: Cells where the configuration is missing or the configuration value was not retrieved.
- White: Default state.



## Filtering Operations

The filter bar is divided into three parts: filter by name, quick filter, and global search. These three methods can be used in combination to quickly find and compare configurations.

### Filter Name

Select a service name from the dropdown menu, and the table will display configurations only for the selected service. The default setting shows all configurations.

### Quick Filter

Filters based on the values in the "Consistency" and "Skip" columns. Select a filtering condition from the dropdown menu. If the selected condition matches the value in a row, that row will be hidden from the table.

If the "Invert" box is checked, the table will only display the rows that match the condition.

### Global Search

Enter the search content in the input box and click the search button to perform a string search across all table data. Cells with matching values will be highlighted, and rows without matching values will be hidden.

### Reset Conditions

Click the reset button next to the search button to reset all filtering conditions and clear the search input box, displaying the full table content.



## Editing Operations

The program does not modify the original configurations. The skip list is stored in the local file `config\config_skip.txt`.

### Copy Content

Click or drag a cell with the mouse. In the right-click context menu or the toolbar, select "Copy" to copy the selected data to the system clipboard.

### Export List

Export the data currently displayed in the table to a file. From the "Edit" menu bar or the table's right-click menu, select "Export". In the file save window, choose the export format. Supports `JSON` or `CSV` formats. Click save to export.

### Ignore Operation

Users can customize which configuration rows to ignore. Click or drag a cell with the mouse, and in the right-click context menu or the toolbar, select "Skip". The configuration row will be marked as ignored. The quick filter can then be applied to hide the ignored configuration rows.

To undo the ignore operation, similarly select "Unskip". The configuration row will be removed from the skip list.



## Help Operations

This includes viewing logs, checking for program updates, and viewing program information.

### View Logs

Select "View Logs" from the "Help" menu or quick toolbar to open the log viewing window:

![view logs](https://raw.githubusercontent.com/hxz393/ConfigCenterComparer/main/doc/view_logs_en.jpg)

The dropdown box in the upper left corner allows you to select the log level to display. For example, if you select "WARNING", only logs of the WARNING level and above will be displayed, and INFO level log messages will be filtered out.

The "Feedback" button in the lower left corner, when clicked, redirects to the GitHub project Issues page for easy submission of error information.

The "Clear" button in the lower left corner, when clicked, clears the content of the log file. The log files are stored in the `logs` directory. They roll over after reaching 1MB in size, with a maximum of ten files kept.

### Check for Updates

Select "Check Updates" from the "Help" menu to check online for program updates. A popup will inform you of the results.

### About Software

Select "About" from the "Help" menu to pop up the program description and build information.



# Common Issues

When encountering errors in software operation, first check the logs. If it's a connection issue, please check the configuration and retry. Then refer to the solutions for common issues below. Finally, check all [Issues](https://github.com/hxz393/ConfigCenterComparer/issues) to see if the same problem exists. For further assistance, you can submit a new [Issue](https://github.com/hxz393/ConfigCenterComparer/issues) and include relevant logs.



# Update Log

To avoid an overly lengthy update log, only the most recent updates are retained.

## Version 1.0.2 (2023.11.21)

Features:

1. Added a table color switch to address performance degradation due to large data volumes.

Updates:

1. Modified color application logic to improve execution speed;
2. Optimized main thread code to enhance UI stability.



## Version 1.0.1 (2023.11.19)

Updates:

1. Clear filter bar conditions before starting the run to prevent the interface from freezing when running again;
2. Optimize the text displayed in logs.



## Version 1.0.0 (2023.11.19)

First release.

