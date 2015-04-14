Python API for netcraft.com 
========


Usage 
========

Import the class: 

```python
from NetcraftAPI import NetcraftAPI
```

Then, search for a specific domain: 


```python
res = NetcraftAPI({'verbose': True}).search('microsoft.com')
print res
```

Result is an array of all subdomains. 

Contributing
=======

Feel free to open issues, contribute and submit your Pull Requests. 
You can also ping me on Twitter (@PaulWebSec)