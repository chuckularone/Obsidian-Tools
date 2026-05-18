<%*
let offset = await tp.system.prompt("Offset (days):", "0");
offset = Number(offset);
%>

**==<% tp.date.now("dddd", offset) %>==**
[[My Notes]] - [[<% tp.date.now("YYYY/MMMM_YYYY", offset) %>|<% tp.date.now("MMMM YYYY", offset) %>]] - [[<% tp.date.now("YYYY/MM_MMMM/YYYY_MM_DD", offset - 1) %>|Yesterday]] - [[<% tp.date.now("YYYY/MM_MMMM/YYYY_MM_DD", offset + 1) %>|Tomorrow]]

> [!abstract] To do
> todo items

> [!info] Health Data 
>Health Notes/Blood Pressure
>
>🏋️ ?? x ??


