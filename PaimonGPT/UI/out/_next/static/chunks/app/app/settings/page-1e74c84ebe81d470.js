(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[7378],{60606:function(t,n,e){var o={"./Chart/page":[40250,6281,6161,3995,7986,250],"./DBQA/page":[46282,6281,6161,6728],"./Programming/page":[35985,6281,6161,3995,7986,5985],"./Universal/page":[96415,6281,6161,3995,7986,6415]};function a(t){if(!e.o(o,t))return Promise.resolve().then(function(){var n=Error("Cannot find module '"+t+"'");throw n.code="MODULE_NOT_FOUND",n});var n=o[t],a=n[0];return Promise.all(n.slice(1).map(e.e)).then(function(){return e(a)})}a.keys=function(){return Object.keys(o)},a.id=60606,t.exports=a},24612:function(t,n,e){Promise.resolve().then(e.bind(e,95513))},65328:function(t,n,e){"use strict";e.d(n,{Aq:function(){return a},JR:function(){return l},KD:function(){return p},PW:function(){return d},YC:function(){return r},ZF:function(){return u},dJ:function(){return i},fQ:function(){return c},pm:function(){return s},sr:function(){return f}});var o=e(13650);async function a(){let t={method:"GET",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")}},n=await (0,o.d)("/ai/app/list",t);return n?n.list:[]}async function i(t){let n={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({app_id:t})};return await (0,o.d)("/ai/app/info",n)}async function r(t,n){let e=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"",a=arguments.length>3?arguments[3]:void 0,i=arguments.length>4&&void 0!==arguments[4]?arguments[4]:[],r={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({app_id:t,name:n,description:e,llm_name:a,kbs:i})};return await (0,o.d)("/ai/app/info/modify",r)}async function u(t){let n={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({app_id:t})};return await (0,o.d)("/ai/app/create/from_appstore",n)}async function c(t,n){let e=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[],a={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({name:t,llm_name:n,kbs:e})};return await (0,o.d)("/ai/app/create",a)}async function s(t){let n={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({app_id:t})};return await (0,o.d)("/ai/app/delete",n)}async function p(t){let n={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({app_id:t})},e=await (0,o.d)("/ai/app/chat/list",n);return e?e.list:[]}async function l(t){let n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:void 0,e={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({app_id:t,name:n})};return await (0,o.d)("/ai/app/chat/create",e)}async function d(t){let n={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({chat_id:t})};return await (0,o.d)("/ai/app/chat/delete",n)}async function f(t){let n={method:"POST",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")},body:JSON.stringify({chat_id:t})},e=await (0,o.d)("/ai/app/chat/message/list",n);return e?e.list:[]}},13650:function(t,n,e){"use strict";async function o(t,n){let e=await fetch(t,n);return await e.json()}e.d(n,{d:function(){return o}})},95513:function(t,n,e){"use strict";e.r(n),e.d(n,{default:function(){return u}});var o=e(57437),a=e(24033),i=e(2265),r=e(65328);function u(){let t=(0,a.useSearchParams)().get("appid"),[n,u]=(0,i.useState)({}),[c,s]=(0,i.useState)("div");async function p(){let n=await (0,r.dJ)(t);if(n){u(n);let t=n.module_name||"Universal";s((0,i.lazy)(()=>e(60606)("./".concat(t,"/page"))))}}return(0,i.useEffect)(()=>{p()},[]),(0,o.jsx)(o.Fragment,{children:(0,o.jsx)(c,{appInfo:n,setAppInfo:u})})}},30622:function(t,n,e){"use strict";var o=e(2265),a=Symbol.for("react.element"),i=Symbol.for("react.fragment"),r=Object.prototype.hasOwnProperty,u=o.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,c={key:!0,ref:!0,__self:!0,__source:!0};function s(t,n,e){var o,i={},s=null,p=null;for(o in void 0!==e&&(s=""+e),void 0!==n.key&&(s=""+n.key),void 0!==n.ref&&(p=n.ref),n)r.call(n,o)&&!c.hasOwnProperty(o)&&(i[o]=n[o]);if(t&&t.defaultProps)for(o in n=t.defaultProps)void 0===i[o]&&(i[o]=n[o]);return{$$typeof:a,type:t,key:s,ref:p,props:i,_owner:u.current}}n.Fragment=i,n.jsx=s,n.jsxs=s},57437:function(t,n,e){"use strict";t.exports=e(30622)},24033:function(t,n,e){t.exports=e(15313)}},function(t){t.O(0,[2971,4938,1744],function(){return t(t.s=24612)}),_N_E=t.O()}]);