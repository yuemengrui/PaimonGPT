"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[7986],{18039:function(t,e,n){n.d(e,{B:function(){return r}});var i=n(13650);async function r(){let t={method:"GET",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")}},e=await (0,i.d)("/ai/llm/list",t);return(console.log("llm list response",e),e)?e.data:[]}},72194:function(t,e,n){n.d(e,{Bv:function(){return a},D6:function(){return u},If:function(){return l},SE:function(){return c},Yk:function(){return r},xs:function(){return s},zM:function(){return o}});var i=n(13650);async function r(){let t={method:"GET",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")}},e=await (0,i.d)("/ai/kb/list",t);return(console.log("response",e),e)?e.list:[]}async function a(t,e){let n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"",r={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({name:t,embedding_model:e,description:n})};return await (0,i.d)("/ai/kb/create",r)}async function o(t){let e={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({kb_id:t})};return await (0,i.d)("/ai/kb/delete",e)}async function l(t){let e={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({kb_id:t})},n=await (0,i.d)("/ai/kb/file/list",e);return(console.log("response",n),n)?n.list:[]}async function s(t,e,n){let r={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({kb_id:t,method_id:e,files:n})};console.log("response",await (0,i.d)("/ai/kb/file/import",r))}async function c(t){let e={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({file_id:t})},n=await (0,i.d)("/ai/kb/file/chunks",e);return(console.log("response",n),n)?n.list:[]}async function u(t){let e={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({data_id:t})};return await (0,i.d)("/ai/kb/file/delete",e)}},58681:function(t,e,n){n.d(e,{Z:function(){return f}});var i=n(57437),r=n(26621),a=n(56641),o=n(93309),l=n(74261),s=n(9304),c=n(2265),u=n(18039),d=n(72194),h=n(65328),m=n(73623);function f(t){let{appInfo:e,setAppInfo:n}=t,f=(0,m.p)(),p=[];e.kbs.map(t=>p.push(t.name));let[g,x]=(0,c.useState)([]),[y,v]=(0,c.useState)([]),[j,b]=(0,c.useState)(e.name),[w,S]=(0,c.useState)(e.description),[k,N]=(0,c.useState)(e.llm_name),[O,C]=(0,c.useState)(p);async function _(){let t=[];O.length>0&&O.map(e=>{let n=y.filter(t=>t.name===e)[0];t.push(n)});let i=await (0,h.YC)(e.id,j,w,k,t);i?i.errmsg?f({title:"保存失败",description:i.errmsg,status:"error",position:"top",duration:2e3}):(f({title:"保存成功",status:"success",position:"top",duration:2e3}),n({...e,name:j,llm_name:k})):f({title:"保存失败",status:"error",position:"top",duration:2e3})}return(0,c.useEffect)(()=>{(async function(){let t=await (0,u.B)();t&&t.length>0&&x(t);let e=await (0,d.Yk)();e&&e.length>0&&v(e)})()},[]),(0,i.jsxs)("div",{className:"w-full flex flex-1 px-6 py-6 flex-col ml-12 mt-12",children:[(0,i.jsx)("div",{children:(0,i.jsxs)(r.k,{gap:20,alignItems:"center",children:[(0,i.jsx)("div",{className:"text-lg",children:"应用名称"}),(0,i.jsx)("input",{className:"border border-gray-200 rounded w-[256px] h-[40px] indent-4 text-lg",maxLength:32,value:j,onChange:t=>{"\n"!==t.target.value&&b(t.target.value)}})]})}),(0,i.jsx)("div",{className:"mt-10",children:(0,i.jsxs)(r.k,{gap:20,alignItems:"center",children:[(0,i.jsx)("div",{className:"text-lg",children:"应用描述"}),(0,i.jsx)("input",{className:"border border-gray-200 rounded w-[256px] h-[40px] indent-4 text-lg",maxLength:32,value:w,onChange:t=>{"\n"!==t.target.value&&S(t.target.value)}})]})}),(0,i.jsx)("div",{className:"mt-10",children:(0,i.jsxs)(r.k,{gap:20,alignItems:"center",children:[(0,i.jsx)("div",{className:"text-lg",children:"应用类型"}),(0,i.jsx)("div",{children:"自建应用"})]})}),(0,i.jsx)("div",{className:"mt-10",children:(0,i.jsxs)(r.k,{gap:20,alignItems:"center",children:[(0,i.jsx)("div",{className:"text-lg",children:"大模型"}),(0,i.jsx)("div",{className:"ml-[20px]",children:(0,i.jsx)(a.P,{w:"256px",onChange:t=>{N(t.target.value)},value:k,children:g.map(t=>(0,i.jsx)("option",{children:t.model_name},t.model_name))})})]})}),(0,i.jsx)("div",{className:"mt-10",children:(0,i.jsxs)(r.k,{gap:20,alignItems:"center",children:[(0,i.jsx)("div",{className:"text-lg",children:"关联知识库"}),(0,i.jsx)(o.c,{onChange:t=>C(t),defaultValue:O,children:(0,i.jsx)(l.K,{spacing:5,direction:"column",children:y.map(t=>(0,i.jsx)(s.X,{value:t.name,children:t.name},t.id))})})]})}),(0,i.jsx)("button",{onClick:_,className:"w-[128px] h-[40px] bg-blue-400/90 text-white rounded-lg ml-[160px] mt-12 border hover:bg-blue-400 hover:shadow-[0_0_2px_2px_rgba(147,197,253,0.6)]",children:"保存"})]})}},91172:function(t,e,n){n.d(e,{w_:function(){return s}});var i=n(2265),r={color:void 0,size:void 0,className:void 0,style:void 0,attr:void 0},a=i.createContext&&i.createContext(r),o=function(){return(o=Object.assign||function(t){for(var e,n=1,i=arguments.length;n<i;n++)for(var r in e=arguments[n])Object.prototype.hasOwnProperty.call(e,r)&&(t[r]=e[r]);return t}).apply(this,arguments)},l=function(t,e){var n={};for(var i in t)Object.prototype.hasOwnProperty.call(t,i)&&0>e.indexOf(i)&&(n[i]=t[i]);if(null!=t&&"function"==typeof Object.getOwnPropertySymbols)for(var r=0,i=Object.getOwnPropertySymbols(t);r<i.length;r++)0>e.indexOf(i[r])&&Object.prototype.propertyIsEnumerable.call(t,i[r])&&(n[i[r]]=t[i[r]]);return n};function s(t){return function(e){return i.createElement(c,o({attr:o({},t.attr)},e),function t(e){return e&&e.map(function(e,n){return i.createElement(e.tag,o({key:n},e.attr),t(e.child))})}(t.child))}}function c(t){var e=function(e){var n,r=t.attr,a=t.size,s=t.title,c=l(t,["attr","size","title"]),u=a||e.size||"1em";return e.className&&(n=e.className),t.className&&(n=(n?n+" ":"")+t.className),i.createElement("svg",o({stroke:"currentColor",fill:"currentColor",strokeWidth:"0"},e.attr,r,c,{className:n,style:o(o({color:t.color||e.color},e.style),t.style),height:u,width:u,xmlns:"http://www.w3.org/2000/svg"}),s&&i.createElement("title",null,s),t.children)};return void 0!==a?i.createElement(a.Consumer,null,function(t){return e(t)}):e(r)}},26621:function(t,e,n){n.d(e,{k:function(){return o}});var i=n(58250),r=n(82184),a=n(57437),o=(0,i.G)(function(t,e){let{direction:n,align:i,justify:o,wrap:l,basis:s,grow:c,shrink:u,...d}=t;return(0,a.jsx)(r.m.div,{ref:e,__css:{display:"flex",flexDirection:n,alignItems:i,justifyContent:o,flexWrap:l,flexBasis:s,flexGrow:c,flexShrink:u},...d})});o.displayName="Flex"},45663:function(t,e,n){n.d(e,{lq:function(){return r},qq:function(){return a}});var i=n(2265);function r(...t){return e=>{t.forEach(t=>{!function(t,e){if(null!=t){if("function"==typeof t){t(e);return}try{t.current=e}catch(n){throw Error(`Cannot assign value '${e}' to ref '${t}'`)}}}(t,e)})}}function a(...t){return(0,i.useMemo)(()=>r(...t),t)}},73623:function(t,e,n){n.d(e,{p:function(){return l}});var i=n(6161),r=n(8936),a=n(12704),o=n(2265);function l(t){let{theme:e}=(0,a.uP)(),n=(0,i.OX)();return(0,o.useMemo)(()=>(0,r.Cj)(e.direction,{...n,...t}),[t,e.direction,n])}}}]);