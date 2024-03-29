"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[753],{5523:function(e,t,n){async function r(e,t){let n;let r=e.getReader();for(;!(n=await r.read()).done;)t(n.value)}function a(){return{data:"",event:"",id:"",retry:void 0}}n.d(t,{L:function(){return o}});var i=function(e,t){var n={};for(var r in e)Object.prototype.hasOwnProperty.call(e,r)&&0>t.indexOf(r)&&(n[r]=e[r]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols)for(var a=0,r=Object.getOwnPropertySymbols(e);a<r.length;a++)0>t.indexOf(r[a])&&Object.prototype.propertyIsEnumerable.call(e,r[a])&&(n[r[a]]=e[r[a]]);return n};let s="text/event-stream",l="last-event-id";function o(e,t){var{signal:n,headers:o,onopen:d,onmessage:u,onclose:p,onerror:h,openWhenHidden:x,fetch:m}=t,g=i(t,["signal","headers","onopen","onmessage","onclose","onerror","openWhenHidden","fetch"]);return new Promise((t,i)=>{let f;let b=Object.assign({},o);function j(){f.abort(),document.hidden||N()}b.accept||(b.accept=s),x||document.addEventListener("visibilitychange",j);let y=1e3,v=0;function w(){document.removeEventListener("visibilitychange",j),window.clearTimeout(v),f.abort()}null==n||n.addEventListener("abort",()=>{w(),t()});let _=null!=m?m:window.fetch,k=null!=d?d:c;async function N(){var n,s;f=new AbortController;try{let n,i,o,c;let d=await _(e,Object.assign(Object.assign({},g),{headers:b,signal:f.signal}));await k(d),await r(d.body,(s=function(e,t,n){let r=a(),i=new TextDecoder;return function(s,l){if(0===s.length)null==n||n(r),r=a();else if(l>0){let n=i.decode(s.subarray(0,l)),a=l+(32===s[l+1]?2:1),o=i.decode(s.subarray(a));switch(n){case"data":r.data=r.data?r.data+"\n"+o:o;break;case"event":r.event=o;break;case"id":e(r.id=o);break;case"retry":let c=parseInt(o,10);isNaN(c)||t(r.retry=c)}}}}(e=>{e?b[l]=e:delete b[l]},e=>{y=e},u),c=!1,function(e){void 0===n?(n=e,i=0,o=-1):n=function(e,t){let n=new Uint8Array(e.length+t.length);return n.set(e),n.set(t,e.length),n}(n,e);let t=n.length,r=0;for(;i<t;){c&&(10===n[i]&&(r=++i),c=!1);let e=-1;for(;i<t&&-1===e;++i)switch(n[i]){case 58:-1===o&&(o=i-r);break;case 13:c=!0;case 10:e=i}if(-1===e)break;s(n.subarray(r,e),o),r=i,o=-1}r===t?n=void 0:0!==r&&(n=n.subarray(r),i-=r)})),null==p||p(),w(),t()}catch(e){if(!f.signal.aborted)try{let t=null!==(n=null==h?void 0:h(e))&&void 0!==n?n:y;window.clearTimeout(v),v=window.setTimeout(N,t)}catch(e){w(),i(e)}}}N()})}function c(e){let t=e.headers.get("content-type");if(!(null==t?void 0:t.startsWith(s)))throw Error(`Expected content-type to be ${s}, Actual: ${t}`)}},1823:function(e,t,n){n.r(t),n.d(t,{default:function(){return c}});var r=n(57437),a=n(2265),i=n(81768),s=n(65328),l=n(73623),o=n(71647);function c(e){let{appInfo:t}=e,n=(0,l.p)(),[c,d]=(0,a.useState)([]),[u,p]=(0,a.useState)(null);async function h(){let e=await (0,s.KD)(t.id);e&&e.length>0?(d(e),p(e[0].id)):(d([]),p(null))}async function x(){let e=await (0,s.JR)(t.id);e?e.errmsg?n({title:"失败",description:e.errmsg,status:"error",position:"top",duration:2e3}):n({title:"成功",status:"success",position:"top",duration:2e3}):n({title:"失败",status:"error",position:"top",duration:2e3}),await h()}async function m(e){let t=await (0,s.PW)(e);t?t.errmsg?n({title:"删除失败",description:t.errmsg,status:"error",position:"top",duration:2e3}):n({title:"删除成功",status:"success",position:"top",duration:2e3}):n({title:"删除失败",status:"error",position:"top",duration:2e3}),await h()}return(0,a.useEffect)(()=>{h()},[]),(0,r.jsx)("div",{className:"flex h-full",style:{maxHeight:"calc(100vh - 68px)",minHeight:"calc(100vh - 76px)"},children:(0,r.jsxs)("div",{className:"flex flex-1 border border-gray-200 bg-white rounded-3xl mt-1 mr-2 ml-2 mb-2 overflow-y-auto h-full",children:[(0,r.jsx)(i.Z,{appName:t.name,chatList:c,selectChatId:u,setSelectChatId:p,newChat:x,deleteChat:m}),(0,r.jsx)("div",{className:"w-[1px] h-full bg-gray-200"}),u&&(0,r.jsx)(o.Z,{appInfo:t,chat_id:u,chat_name:c.length&&c.filter(e=>e.id===u)[0].name||"新对话"})]})})}},81768:function(e,t,n){n.d(t,{Z:function(){return y}});var r=n(57437),a=n(211),i=n(26621),s=n(30954),l=n(76526),o=n(72647),c=n(3391),d=n(81629),u=n(4159),p=n(88610),h=n(71504),x=n(89348),m=n(52410),g=n(8574),f=n(19734),b=n(73623),j=n(2265);function y(e){let{appName:t,chatList:n,selectChatId:y,setSelectChatId:v,newChat:w,deleteChat:_}=e,k=(0,b.p)(),[N,C]=(0,j.useState)(!1),[O,S]=(0,j.useState)(null);async function I(){_(O),C(!1)}return(0,r.jsxs)("div",{className:"w-[256px] rounded-l-3xl px-6 py-6",children:[(0,r.jsxs)(i.k,{alignItems:"center",children:[(0,r.jsx)("div",{className:"text-3xl border rounded-lg border-gray-100 shadow-[2px_2px_2px_2px_rgba(0,0,0,0.2)]",children:(0,r.jsx)(a.Cp6,{})}),(0,r.jsx)("div",{className:"ml-4",children:t})]}),(0,r.jsx)(i.k,{alignItems:"center",mt:12,children:(0,r.jsx)("button",{onClick:w,className:"w-full border rounded-lg border-gray-100 shadow-[0_0_2px_2px_rgba(0,0,0,0.1)] px-4 py-1 hover:text-pink-400 hover:bg-pink-100",children:(0,r.jsxs)(i.k,{alignItems:"center",textAlign:"center",justifyContent:"center",children:[(0,r.jsx)(x.Sjn,{}),(0,r.jsx)("span",{className:"ml-2",children:"新对话"})]})})}),(0,r.jsx)(i.k,{alignItems:"center",mt:6,direction:"column",children:n.map(e=>(0,r.jsx)("button",{className:"".concat(y===e.id?"shadow-[0_0_1px_1px_rgba(244,114,182,0.2)] text-pink-400 bg-pink-100":"hover:text-pink-300 hover:bg-blue-100"," w-full rounded-lg px-2 py-2 mt-4"),onClick:()=>v(e.id),children:(0,r.jsxs)(i.k,{position:"relative",alignItems:"center",children:[(0,r.jsx)(x.Sjn,{className:"ml-2"}),(0,r.jsx)("span",{className:"ml-2 max-w-[96px] truncate overflow-hidden",children:e.name||"新对话"}),(0,r.jsx)("div",{onClick:t=>{e.id,t.stopPropagation(),k({title:"该功能正在实现中，请稍等...",status:"warning",position:"top",duration:2e3})},className:"absolute right-2",children:(0,r.jsx)(f.Z,{label:e.isTopping?"取消置顶":"置顶",children:(0,r.jsx)(g.HYc,{})})}),(0,r.jsx)("div",{onClick:t=>{var n;n=e.id,t.stopPropagation(),C(!0),S(n)},className:"absolute -right-2 -top-2 text-sm hover:text-red-600",children:(0,r.jsx)(m.j7p,{})})]})},e.id))}),N&&(0,r.jsxs)(s.u_,{isOpen:!0,onClose:()=>C(!1),children:[(0,r.jsx)(l.Z,{}),(0,r.jsxs)(o.h,{children:[(0,r.jsx)(c.x,{children:"确认删除该聊天记录吗？"}),(0,r.jsx)(d.o,{}),(0,r.jsx)(u.f,{children:(0,r.jsx)("div",{className:"text-center",children:"删除后数据将无法恢复"})}),(0,r.jsx)(p.m,{children:(0,r.jsx)(h.z,{border:"1px",borderColor:"gray.200",onClick:I,children:"确认删除"})})]})]})]})}},71647:function(e,t,n){n.d(t,{Z:function(){return p}});var r=n(57437),a=n(6806),i=n(73342),s=n(2265),l=n(37600),o=n(26621),c=n(65328),d=n(5618),u=n(5523);function p(e){let{appInfo:t,chat_id:n,chat_name:p,prompt_instruction:h=""}=e,[x,m]=(0,s.useState)([]),[g,f]=(0,s.useState)(!1);async function b(){let e=await (0,c.sr)(n);e&&e.length&&m(e)}(0,s.useEffect)(()=>{b()},[]);let j=e=>{m(t=>[...t,e])},y=e=>{m(t=>[...t.slice(0,-1),e])};async function v(e){let r={id:(0,d.Z)(),role:"user",type:"text",content:e};j(r);let a={id:(0,d.Z)(),role:"assistant",type:"text",content:"正在思考中...",response:{}};j(a),f(!0),await (0,u.L)("/ai/llm/chat",{openWhenHidden:!0,method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({app_id:t.id,chat_id:n,uid:r.id,answer_uid:a.id,prompt:h+r.content,model_name:t.llm_name}),onmessage(e){try{let t=JSON.parse(e.data);f(!1),y({id:a.id,role:a.role,type:"text",content:t.answer,response:t})}catch(e){console.log(e)}},onerror(e){throw f(!1),y({id:a.id,role:a.role,type:"text",content:"抱歉！服务繁忙！请稍后重试！",response:{}}),e}})}return(0,r.jsxs)("div",{className:"w-full relative",children:[(0,r.jsx)("div",{className:"h-[64px] px-6 py-5",children:(0,r.jsxs)(o.k,{gap:3,children:[(0,r.jsx)("div",{children:p}),(0,r.jsx)(l.Z,{text:x.length+"条记录"})]})}),(0,r.jsx)("div",{className:"h-[1px] w-full bg-gray-200"}),x.length&&(0,r.jsx)(i.Z,{messageList:x,stream_generate:v,waitingReply:g}),(0,r.jsx)(a.Z,{stream_generate:v})]})}}}]);