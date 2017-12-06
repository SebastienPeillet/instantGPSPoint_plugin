# instantGPSPoint_plugin
Intramaps Roam plugin - Create a toolbar with buttons to catch instant GPS point with attribute.

### Install
Download or clone the repository in your Intramaps_Roam folder like this:
  * Intramaps_Roam/plugins/instantGPSPoint_plugin

It's important to keep the __plugin_ at the end of the folder name.

### Use
To activate the plugin for a project, you need to edit your project.config file and add these lines :
> plugins:  
>  \- instantGPSPoint_plugin

Then you need to indicate your current work layer, the attribute field and the different attribute proposals :
> gpspointlayer:  
>  \- layer name  
> gpspointattr:  
>  \- attribute field name  
> gpspointoption:  
>  \- option 1 (string)  
>  \- option 2 (string)  
>  \- etc

Futhermore you can add a time field in the layer to record time in addition to the coordinates :
> gpspointtime: (optionnal field name for time)  
>  \- time field name

### Example
A project.config file example :

plugins:  
\- instantGPSPoint_plugin  
gpspointlayer:  
\- point_gps  
gpspointattr:  
\- description  
gpspointoption:  
\- Option1  
\- Option2  
\- Option3  
\- Option4  
\- Option5  

Will create this toolbar :

![alt text](https://raw.githubusercontent.com/SebastienPeillet/raw/master/instantGPSPoint_plugin/master/Intramaps_example.png "toolbar_example")  

Each button will create a new point feature with the gps coordinates and an attribute (\"Option1\", \"Option2\", etc) in the _description_ field of the point_gps layer.  
The time will not be recorded unless you indicated also an time field like :  

gpspointtime:  
\- recordTime

Then the record time will be save in the _recordTime_ field.