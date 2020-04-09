# TodayCVE

A tool to get the new CVEs.<br>
The CVEs update in https://cassandra.cerias.purdue.edu/CVE_changes/today.html .<br>
And it's description in http://cve.mitre.org/cgi-bin/cvename.cgi?name={id} .<br>
The tool will get the discription and translate it in chinese.<br>
Translate API is google translate.<br>

**4.1: Add a database to save the cve data.{date,CVEId,URL,description_En,description_Zh}**<br>
Reduce the time to get the information which database has.<br>

**4.9: Add the ability to search**<br>
Excute: SELECT * FROM CVEinfo WHERE description_En LIKE '%{}%' OR description_Zh LIKE '%{}%'

## Usage

```shell
cd TodayCVE
python TodayCVE.py
```

## Example

```shell
python TodayCVE.py -u
```

```shell
python TodayCVE.py -s linux
```