# Savant-web
This serves as the web front-end for Savant. Use it to identify and
categorize deltas.

# Usage
* Run `savant-web.py`
* Point your web browser at http://localhost:5000

# Profiling
To measure performance, use the line profiler. At this time, it must be
manually added to each sub module for testing only. For instance, we
can't set it to descend into savant. So in savant (for instance):

```python
import flask_debugtoolbar
from flask_debugtoolbar_lineprofilerpanel.profile import line_profile

# ...somewhere in the module, right above the function to profile
@line_profile
```
