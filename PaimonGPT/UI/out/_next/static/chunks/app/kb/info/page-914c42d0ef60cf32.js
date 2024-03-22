(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[3792],{22389:function(e,t,n){Promise.resolve().then(n.bind(n,60007))},13650:function(e,t,n){"use strict";async function i(e,t){let n=await fetch(e,t);return await n.json()}n.d(t,{d:function(){return i}})},72194:function(e,t,n){"use strict";n.d(t,{Bv:function(){return r},D6:function(){return d},If:function(){return l},SE:function(){return c},Yk:function(){return s},xs:function(){return o},zM:function(){return a}});var i=n(13650);async function s(){let e={method:"GET",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")}},t=await (0,i.d)("/ai/kb/list",e);return(console.log("response",t),t)?t.list:[]}async function r(e,t){let n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"",s={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({name:e,embedding_model:t,description:n})};return await (0,i.d)("/ai/kb/create",s)}async function a(e){let t={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({kb_id:e})};return await (0,i.d)("/ai/kb/delete",t)}async function l(e){let t={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({kb_id:e})},n=await (0,i.d)("/ai/kb/file/list",t);return(console.log("response",n),n)?n.list:[]}async function o(e,t,n){let s={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({kb_id:e,method_id:t,files:n})};console.log("response",await (0,i.d)("/ai/kb/file/import",s))}async function c(e){let t={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({file_id:e})},n=await (0,i.d)("/ai/kb/file/chunks",t);return(console.log("response",n),n)?n.list:[]}async function d(e){let t={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({data_id:e})};return await (0,i.d)("/ai/kb/file/delete",t)}},60007:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return R}});var i=n(57437),s=n(24033),r=n(26621),a=n(211),l=n(2265),o=n(73623),c=n(15982),d=n(10056),u=n(22043),x=n(52736),h=n(17885),m=n(97464),p=n(32527),f=n(30954),g=n(76526),j=n(72647),b=n(3391),y=n(81629),v=n(4159),_=n(88610),N=n(71504),w=n(19241),k=n(72194),S=n(16691),T=n.n(S);function C(e){let{kb_id:t}=e,n=(0,o.p)(),[s,a]=(0,l.useState)([]),[S,C]=(0,l.useState)(!1),[A,O]=(0,l.useState)(null),[z,I]=(0,l.useState)(!1),[E,G]=(0,l.useState)({});async function P(){a(await (0,k.If)(t))}async function R(e){console.log(e),e.detail=await (0,k.SE)(e.id),console.log(e),G(e),I(!0)}async function F(){let e=await (0,k.D6)(A.id);e&&e.msg?n({title:"删除成功",status:"success",position:"top",duration:2e3}):n({title:"删除失败",description:e.errmsg,status:"error",position:"top",duration:2e3}),C(!1),O(null)}return(0,l.useEffect)(()=>{P()},[]),(0,i.jsxs)("div",{className:"w-full",children:[z?(0,i.jsxs)("div",{children:[(0,i.jsx)("button",{className:"mt-2 ml-2 text-blue-400",onClick:function(){G({}),I(!1)},children:"返回"}),(0,i.jsxs)(r.k,{gap:12,ml:12,mt:12,children:[(0,i.jsxs)("div",{className:"text-xl",children:["文件名：",E.file_name]}),(0,i.jsxs)("div",{className:"text-xl",children:["数据总量：",E.chunk_total]})]}),(0,i.jsx)("ul",{className:"mt-12 px-12",children:E.detail.map(e=>(0,i.jsxs)("div",{className:"list-decimal py-2 mt-12 text-sm whitespace-pre-wrap",children:[(0,i.jsxs)(r.k,{gap:6,fontSize:"large",children:[(0,i.jsxs)("div",{children:["第",e.page,"页"]}),(0,i.jsxs)("div",{children:["类型: ",e.type]}),"table"===e.type&&(0,i.jsxs)("div",{children:["Table_Caption: ",e.content||"None"]}),"figure"===e.type&&(0,i.jsxs)("div",{children:["Figure_Caption: ",e.content||"None"]})]}),(0,i.jsxs)("div",{className:"mt-2 border-2 px-2 py-2 border-dashed border-blue-400",children:["text"===e.type&&(0,i.jsx)("div",{children:e.content}),"table"===e.type&&(0,i.jsxs)(r.k,{mt:2,children:[(0,i.jsx)(T(),{src:e.url,alt:"image",width:600,height:600}),(0,i.jsx)("div",{dangerouslySetInnerHTML:{__html:e.html}})]}),"figure"===e.type&&(0,i.jsx)(T(),{src:e.url,alt:"image",width:600,height:600})]})]},e.id))})]}):(0,i.jsx)(c.x,{mt:2,minH:"70vh",children:s.length>0?(0,i.jsxs)(d.i,{fontSize:"sm",children:[(0,i.jsx)(u.h,{children:(0,i.jsxs)(x.Tr,{children:[(0,i.jsx)(h.Th,{children:"文件名"}),(0,i.jsx)(h.Th,{children:"数据总量"}),(0,i.jsx)(h.Th,{children:"上传时间"}),(0,i.jsx)(h.Th,{children:"状态"}),(0,i.jsx)(h.Th,{})]})}),(0,i.jsx)(m.p,{children:s.map(e=>(0,i.jsxs)(x.Tr,{cursor:"pointer",_hover:{bg:"blue.50"},onClick:()=>R(e),children:[(0,i.jsx)(p.Td,{maxW:["300px","400px"],overflow:"overlay",children:e.file_name}),(0,i.jsx)(p.Td,{children:e.data_total}),(0,i.jsx)(p.Td,{children:e.create_time}),(0,i.jsx)(p.Td,{children:e.status}),(0,i.jsx)(p.Td,{children:(0,i.jsx)(w.qy0,{className:"hover:text-red-600",onClick:t=>{t.stopPropagation(),O(e),C(!0)}})})]},e.id))})]}):(0,i.jsx)("div",{className:"text-center mt-32",children:"知识库中还没有数据，请先导入数据"})}),S&&(0,i.jsxs)(f.u_,{isOpen:!0,onClose:()=>C(!1),children:[(0,i.jsx)(g.Z,{}),(0,i.jsxs)(j.h,{children:[(0,i.jsxs)(b.x,{children:["确认删除 ",(0,i.jsx)("span",{className:"text-red-600",children:A.file_name})," 吗？"]}),(0,i.jsx)(y.o,{}),(0,i.jsx)(v.f,{children:(0,i.jsx)("div",{className:"text-center",children:"删除后数据将无法恢复"})}),(0,i.jsx)(_.m,{children:(0,i.jsx)(N.z,{border:"1px",borderColor:"gray.200",onClick:F,children:"确认删除"})})]})]})]})}var A=n(58250),O=n(82184),z=(0,A.G)(function(e,t){let{templateAreas:n,gap:s,rowGap:r,columnGap:a,column:l,row:o,autoFlow:c,autoRows:d,templateRows:u,autoColumns:x,templateColumns:h,...m}=e;return(0,i.jsx)(O.m.div,{ref:t,__css:{display:"grid",gridTemplateAreas:n,gridGap:s,gridRowGap:r,gridColumnGap:a,gridAutoColumns:x,gridColumn:l,gridRow:o,gridAutoFlow:c,gridAutoRows:d,gridTemplateRows:u,gridTemplateColumns:h},...m})});z.displayName="Grid";var I=n(13650);async function E(e){let t={method:"POST",headers:{Authorization:localStorage.getItem("Authorization")},body:e},n=await (0,I.d)("/ai/file/upload",t);if(n)return n}var G=e=>{let{uploadFiles:t,setUploadFiles:n,accept:s,fileLimit:r=10}=e,[a,o]=(0,l.useState)(null);return(0,l.useEffect)(()=>{async function e(e){let t=await E(e);t&&n(e=>[...e,t])}if(a){let t=new FormData;t.append("file",a),e(t)}},[a]),(0,i.jsx)("div",{className:"w-[256px] ml-6 mt-6",children:(0,i.jsx)("div",{className:"border rounded-lg border-dashed border-gray-400 px-6 py-6 bg-gray-100",children:t.length<r?(0,i.jsxs)("div",{className:"text-center",children:[(0,i.jsx)("label",{htmlFor:"upload-button",className:"cursor-pointer text-blue-600",children:"选择文件"}),(0,i.jsx)("input",{id:"upload-button",style:{display:"none"},type:"file",accept:s,onChange:e=>{o(e.target.files[0])}}),(0,i.jsx)("div",{className:"mt-3 flex-wrap text-xs text-gray-500",children:"一次选择一个文件"}),(0,i.jsx)("div",{className:"flex-wrap text-xs text-gray-500",children:"最多可以添加10个文件"}),(0,i.jsx)("div",{className:"flex-wrap text-xs text-gray-500",children:"单个文件大小不能超过100M"})]}):(0,i.jsx)("div",{className:"text-center",children:(0,i.jsx)("div",{children:"添加的文件太多了，我吃不下了"})})})})};function P(e){let{kb_id:t}=e,n=(0,o.p)(),[s,a]=(0,l.useState)([]),c=[{id:1,title:"AI智能分段",desc:"AI智能分析数据，自动分段、分句",accept:".txt,.pdf,.docx,.doc,.md"},{id:2,title:"AI智能QA拆分",desc:"AI智能分析数据，自动生成问答对",accept:".txt,.pdf,.docx,.doc,.md"},{id:3,title:"JSON 导入",desc:'批量导入json问答对，格式{"instruction":"问题", "input":"问题的补充数据", "output":"答案"}',accept:".json"}],[d,u]=(0,l.useState)(c[0].id);async function x(){(0,k.xs)(t,d,s),a([]),n({title:"数据导入任务已添加，请耐心等待后台导入完成，稍后可在数据集页面中查看导入的数据",status:"success",position:"top",duration:5e3})}return(0,i.jsxs)("div",{className:"flex flex-col flex-1 px-3 mt-6",children:[(0,i.jsx)("div",{className:"text-xl ml-6 font-semibold italic",children:"数据导入方式"}),(0,i.jsx)(z,{p:6,gridTemplateColumns:["repeat(3,1fr)"],gridGap:6,textAlign:"center",children:c.map(e=>(0,i.jsxs)("div",{className:"".concat(d===e.id?"shadow-[0_0_2px_2px_rgba(244,114,182,0.6)] text-pink-400 bg-pink-100 border-pink-100":"hover:border-blue-300 hover:text-pink-300 hover:bg-blue-100"," border-2 rounded-md py-1"),onClick:()=>{var t;1===(t=e.id)?u(t):n({title:"暂不支持，请选择其他导入方式",status:"warning",position:"top",duration:2e3})},children:[(0,i.jsx)("div",{children:e.title}),(0,i.jsx)("div",{className:"mt-3 flex-wrap text-xs text-gray-500",children:e.desc})]},e.id))}),(0,i.jsx)("div",{className:"w-full h-[1px] bg-gray-200"}),(0,i.jsxs)("div",{className:"flex flex-1",children:[(0,i.jsxs)(r.k,{direction:"column",children:[(0,i.jsx)(G,{uploadFiles:s,setUploadFiles:a,accept:c.filter(e=>e.id===d)[0].accept}),s.length>0&&(0,i.jsx)("button",{onClick:x,className:"bg-blue-400/90 text-white rounded-lg py-2 ml-6 mt-6 border hover:bg-blue-400 hover:shadow-[0_0_2px_2px_rgba(147,197,253,0.6)]",children:"确认导入"})]}),(0,i.jsx)("div",{className:"ml-6 mt-3 mb-3 w-[1px] bg-gray-200"}),s.length>0&&(0,i.jsxs)("div",{className:"ml-6 mt-6",children:[(0,i.jsxs)("div",{className:"text-lg font-semibold",children:["已添加的文件: ",s.length]}),(0,i.jsx)("ul",{className:"mt-6 ml-12",children:s.map(e=>(0,i.jsx)("li",{className:"list-disc py-2",children:e.file_name},e.file_hash))})]})]})]})}function R(){let e=(0,s.useSearchParams)(),t=e.get("kb_id"),n=e.get("kb_name"),o=[{name:"数据集"},{name:"导入数据"},{name:"配置"}],[c,d]=(0,l.useState)(o[0].name);return(0,i.jsx)("div",{className:"flex h-full",style:{maxHeight:"calc(100vh - 60px)",minHeight:"calc(100vh - 76px)"},children:(0,i.jsxs)("div",{className:"flex flex-1 border border-gray-200 bg-white rounded-3xl mt-1 mr-2 ml-2 mb-1",children:[(0,i.jsxs)("div",{className:"w-[156px] rounded-l-3xl",children:[(0,i.jsxs)(r.k,{alignItems:"center",mt:6,ml:4,children:[(0,i.jsx)("div",{className:"text-3xl border rounded-lg border-gray-100 shadow-[2px_2px_2px_2px_rgba(0,0,0,0.2)]",children:(0,i.jsx)(a.Cp6,{})}),(0,i.jsx)("div",{className:"ml-2",children:n})]}),(0,i.jsx)(r.k,{mt:8,direction:"column",gap:2,alignItems:"center",children:o.map(e=>(0,i.jsx)("button",{className:"".concat(c===e.name?"shadow-[0_0_1px_1px_rgba(244,114,182,0.2)] text-pink-400 bg-pink-100":"hover:text-pink-300 hover:bg-blue-100"," w-[128px] rounded-md py-1"),onClick:()=>{d(e.name)},children:e.name},e.name))})]}),(0,i.jsx)("div",{className:"w-[1px] h-full bg-gray-200"}),"数据集"===c&&(0,i.jsx)(C,{kb_id:t}),"导入数据"===c&&(0,i.jsx)(P,{kb_id:t})]})})}},30622:function(e,t,n){"use strict";var i=n(2265),s=Symbol.for("react.element"),r=Symbol.for("react.fragment"),a=Object.prototype.hasOwnProperty,l=i.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,o={key:!0,ref:!0,__self:!0,__source:!0};function c(e,t,n){var i,r={},c=null,d=null;for(i in void 0!==n&&(c=""+n),void 0!==t.key&&(c=""+t.key),void 0!==t.ref&&(d=t.ref),t)a.call(t,i)&&!o.hasOwnProperty(i)&&(r[i]=t[i]);if(e&&e.defaultProps)for(i in t=e.defaultProps)void 0===r[i]&&(r[i]=t[i]);return{$$typeof:s,type:e,key:c,ref:d,props:r,_owner:l.current}}t.Fragment=r,t.jsx=c,t.jsxs=c},57437:function(e,t,n){"use strict";e.exports=n(30622)},24033:function(e,t,n){e.exports=n(15313)},22043:function(e,t,n){"use strict";n.d(t,{h:function(){return l}});var i=n(10056),s=n(58250),r=n(82184),a=n(57437),l=(0,s.G)((e,t)=>{let n=(0,i.p)();return(0,a.jsx)(r.m.thead,{...e,ref:t,__css:n.thead})})},10056:function(e,t,n){"use strict";n.d(t,{i:function(){return x},p:function(){return u}});var i=n(58250),s=n(89839),r=n(50446),a=n(82184),l=n(16465),o=n(310),c=n(57437),[d,u]=(0,o.k)({name:"TableStylesContext",errorMessage:"useTableStyles returned is 'undefined'. Seems you forgot to wrap the components in \"<Table />\" "}),x=(0,i.G)((e,t)=>{let n=(0,s.jC)("Table",e),{className:i,layout:o,...u}=(0,r.Lr)(e);return(0,c.jsx)(d,{value:n,children:(0,c.jsx)(a.m.table,{ref:t,__css:{tableLayout:o,...n.table},className:(0,l.cx)("chakra-table",i),...u})})});x.displayName="Table"},52736:function(e,t,n){"use strict";n.d(t,{Tr:function(){return l}});var i=n(10056),s=n(58250),r=n(82184),a=n(57437),l=(0,s.G)((e,t)=>{let n=(0,i.p)();return(0,a.jsx)(r.m.tr,{...e,ref:t,__css:n.tr})})},97464:function(e,t,n){"use strict";n.d(t,{p:function(){return l}});var i=n(10056),s=n(58250),r=n(82184),a=n(57437),l=(0,s.G)((e,t)=>{let n=(0,i.p)();return(0,a.jsx)(r.m.tbody,{...e,ref:t,__css:n.tbody})})},17885:function(e,t,n){"use strict";n.d(t,{Th:function(){return l}});var i=n(10056),s=n(58250),r=n(82184),a=n(57437),l=(0,s.G)(({isNumeric:e,...t},n)=>{let s=(0,i.p)();return(0,a.jsx)(r.m.th,{...t,ref:n,__css:s.th,"data-is-numeric":e})})},15982:function(e,t,n){"use strict";n.d(t,{x:function(){return l}});var i=n(58250),s=n(82184),r=n(16465),a=n(57437),l=(0,i.G)((e,t)=>{var n;let{overflow:i,overflowX:l,className:o,...c}=e;return(0,a.jsx)(s.m.div,{ref:t,className:(0,r.cx)("chakra-table__container",o),...c,__css:{display:"block",whiteSpace:"nowrap",WebkitOverflowScrolling:"touch",overflowX:null!=(n=null!=i?i:l)?n:"auto",overflowY:"hidden",maxWidth:"100%"}})})},32527:function(e,t,n){"use strict";n.d(t,{Td:function(){return l}});var i=n(10056),s=n(58250),r=n(82184),a=n(57437),l=(0,s.G)(({isNumeric:e,...t},n)=>{let s=(0,i.p)();return(0,a.jsx)(r.m.td,{...t,ref:n,__css:s.td,"data-is-numeric":e})})}},function(e){e.O(0,[6281,9929,6161,8071,5379,2971,4938,1744],function(){return e(e.s=22389)}),_N_E=e.O()}]);