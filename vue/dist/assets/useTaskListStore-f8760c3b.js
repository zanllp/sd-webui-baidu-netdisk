import{cE as r,r as e,m as t,aF as i,cF as d}from"./index-ca58e7a1.js";const v=r("useTaskListStore",()=>{const a=e(new Map),n=t(new i),u=e(3),o=e([]),c=t([]),l=e(-1),s=e(null);return{checkBaiduyunInstalled:async()=>(s.value===null&&(s.value=d()),s.value),baiduyunInstalled:s,pollInterval:u,taskLogMap:a,queue:n,tasks:o,showDirAutoCompletedIdx:l,pendingBaiduyunTaskQueue:c}},{persist:{paths:["pollInterval","tasks"],key:"useTaskListStore-v0.0.1"}});export{v as u};
