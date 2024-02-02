"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[728],{18039:function(e,t,n){n.d(t,{B:function(){return r}});var l=n(13650);async function r(){let e={method:"GET",headers:{"Content-Type":"application/json",Authorization:localStorage.getItem("Authorization")}},t=await (0,l.d)("/ai/llm/list",e);return(console.log("llm list response",t),t)?t.data:[]}},46282:function(e,t,n){n.r(t),n.d(t,{default:function(){return u}});var l=n(57437),r=n(26621),i=n(211),a=n(2265),s=n(73623),o=n(56641),c=n(18039),d=n(65328);function u(e){let{appInfo:t,setAppInfo:n}=e,u=[{name:"配置"}],[m,f]=(0,a.useState)(u[0].name),p=(0,s.p)(),[h,x]=(0,a.useState)([]),[v,b]=(0,a.useState)(t.llm_name);async function g(){let e=await (0,d.YC)(t.id,t.name,t.description,v);e?e.errmsg?p({title:"保存失败",description:e.errmsg,status:"error",position:"top",duration:2e3}):(p({title:"保存成功",status:"success",position:"top",duration:2e3}),n({...t,llm_name:v})):p({title:"保存失败",status:"error",position:"top",duration:2e3})}return(0,a.useEffect)(()=>{(async function(){let e=await (0,c.B)();e&&e.length>0&&x(e)})()},[]),(0,l.jsx)("div",{className:"flex w-full bg-blue-50/30",children:(0,l.jsxs)("div",{className:"flex flex-1 border border-gray-200 bg-white rounded-3xl mt-4 mr-4 ml-4 mb-4",children:[(0,l.jsxs)("div",{className:"w-[156px] rounded-l-3xl",children:[(0,l.jsxs)(r.k,{alignItems:"center",mt:6,ml:4,children:[(0,l.jsx)("div",{className:"text-3xl border rounded-lg border-gray-100 shadow-[2px_2px_2px_2px_rgba(0,0,0,0.2)]",children:(0,l.jsx)(i.Cp6,{})}),(0,l.jsx)("div",{className:"ml-2",children:t.name})]}),(0,l.jsx)(r.k,{mt:8,direction:"column",gap:2,alignItems:"center",children:u.map(e=>(0,l.jsx)("button",{className:"".concat(m===e.name?"shadow-[0_0_1px_1px_rgba(244,114,182,0.2)] text-pink-400 bg-pink-100":"hover:text-pink-300 hover:bg-blue-100"," w-[128px] rounded-md py-1"),onClick:()=>{f(e.name)},children:e.name},e.name))})]}),(0,l.jsx)("div",{className:"w-[1px] h-full bg-gray-200"}),(0,l.jsxs)("div",{className:"w-full flex flex-1 px-6 py-6 flex-col ml-12 mt-12",children:[(0,l.jsx)("div",{children:(0,l.jsxs)(r.k,{gap:20,alignItems:"center",children:[(0,l.jsx)("div",{className:"text-lg",children:"应用名称"}),(0,l.jsx)("div",{children:t.name})]})}),(0,l.jsx)("div",{className:"mt-10",children:(0,l.jsxs)(r.k,{gap:20,alignItems:"center",children:[(0,l.jsx)("div",{className:"text-lg",children:"应用描述"}),(0,l.jsx)("div",{children:t.description})]})}),(0,l.jsx)("div",{className:"mt-10",children:(0,l.jsxs)(r.k,{gap:20,alignItems:"center",children:[(0,l.jsx)("div",{className:"text-lg",children:"大模型"}),(0,l.jsx)("div",{className:"ml-[20px]",children:(0,l.jsx)(o.P,{w:"256px",onChange:e=>{b(e.target.value)},value:v,children:h.map(e=>(0,l.jsx)("option",{children:e.model_name},e.model_name))})})]})}),(0,l.jsx)("button",{onClick:g,className:"w-[128px] h-[40px] bg-blue-400/90 text-white rounded-lg ml-[160px] mt-12 border hover:bg-blue-400 hover:shadow-[0_0_2px_2px_rgba(147,197,253,0.6)]",children:"保存"})]})]})})}},91172:function(e,t,n){n.d(t,{w_:function(){return o}});var l=n(2265),r={color:void 0,size:void 0,className:void 0,style:void 0,attr:void 0},i=l.createContext&&l.createContext(r),a=function(){return(a=Object.assign||function(e){for(var t,n=1,l=arguments.length;n<l;n++)for(var r in t=arguments[n])Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r]);return e}).apply(this,arguments)},s=function(e,t){var n={};for(var l in e)Object.prototype.hasOwnProperty.call(e,l)&&0>t.indexOf(l)&&(n[l]=e[l]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols)for(var r=0,l=Object.getOwnPropertySymbols(e);r<l.length;r++)0>t.indexOf(l[r])&&Object.prototype.propertyIsEnumerable.call(e,l[r])&&(n[l[r]]=e[l[r]]);return n};function o(e){return function(t){return l.createElement(c,a({attr:a({},e.attr)},t),function e(t){return t&&t.map(function(t,n){return l.createElement(t.tag,a({key:n},t.attr),e(t.child))})}(e.child))}}function c(e){var t=function(t){var n,r=e.attr,i=e.size,o=e.title,c=s(e,["attr","size","title"]),d=i||t.size||"1em";return t.className&&(n=t.className),e.className&&(n=(n?n+" ":"")+e.className),l.createElement("svg",a({stroke:"currentColor",fill:"currentColor",strokeWidth:"0"},t.attr,r,c,{className:n,style:a(a({color:e.color||t.color},t.style),e.style),height:d,width:d,xmlns:"http://www.w3.org/2000/svg"}),o&&l.createElement("title",null,o),e.children)};return void 0!==i?l.createElement(i.Consumer,null,function(e){return t(e)}):t(r)}},6036:function(e,t,n){n.d(t,{K:function(){return a},Y:function(){return i}});var l=n(27100),r=n(16465);function i(e){let{isDisabled:t,isInvalid:n,isReadOnly:l,isRequired:i,...s}=a(e);return{...s,disabled:t,readOnly:l,required:i,"aria-invalid":(0,r.Qm)(n),"aria-required":(0,r.Qm)(i),"aria-readonly":(0,r.Qm)(l)}}function a(e){var t,n,i;let a=(0,l.NJ)(),{id:s,disabled:o,readOnly:c,required:d,isRequired:u,isInvalid:m,isReadOnly:f,isDisabled:p,onFocus:h,onBlur:x,...v}=e,b=e["aria-describedby"]?[e["aria-describedby"]]:[];return(null==a?void 0:a.hasFeedbackText)&&(null==a?void 0:a.isInvalid)&&b.push(a.feedbackId),(null==a?void 0:a.hasHelpText)&&b.push(a.helpTextId),{...v,"aria-describedby":b.join(" ")||void 0,id:null!=s?s:null==a?void 0:a.id,isDisabled:null!=(t=null!=o?o:p)?t:null==a?void 0:a.isDisabled,isReadOnly:null!=(n=null!=c?c:f)?n:null==a?void 0:a.isReadOnly,isRequired:null!=(i=null!=d?d:u)?i:null==a?void 0:a.isRequired,isInvalid:null!=m?m:null==a?void 0:a.isInvalid,onFocus:(0,r.v0)(null==a?void 0:a.onFocus,h),onBlur:(0,r.v0)(null==a?void 0:a.onBlur,x)}}},27100:function(e,t,n){n.d(t,{NI:function(){return x},NJ:function(){return h},e:function(){return f}});var l=n(310),r=n(45663),i=n(58250),a=n(89839),s=n(50446),o=n(82184),c=n(16465),d=n(2265),u=n(57437),[m,f]=(0,l.k)({name:"FormControlStylesContext",errorMessage:"useFormControlStyles returned is 'undefined'. Seems you forgot to wrap the components in \"<FormControl />\" "}),[p,h]=(0,l.k)({strict:!1,name:"FormControlContext"}),x=(0,i.G)(function(e,t){let n=(0,a.jC)("Form",e),{getRootProps:l,htmlProps:i,...f}=function(e){let{id:t,isRequired:n,isInvalid:l,isDisabled:i,isReadOnly:a,...s}=e,o=(0,d.useId)(),u=t||`field-${o}`,m=`${u}-label`,f=`${u}-feedback`,p=`${u}-helptext`,[h,x]=(0,d.useState)(!1),[v,b]=(0,d.useState)(!1),[g,j]=(0,d.useState)(!1),y=(0,d.useCallback)((e={},t=null)=>({id:p,...e,ref:(0,r.lq)(t,e=>{e&&b(!0)})}),[p]),_=(0,d.useCallback)((e={},t=null)=>({...e,ref:t,"data-focus":(0,c.PB)(g),"data-disabled":(0,c.PB)(i),"data-invalid":(0,c.PB)(l),"data-readonly":(0,c.PB)(a),id:void 0!==e.id?e.id:m,htmlFor:void 0!==e.htmlFor?e.htmlFor:u}),[u,i,g,l,a,m]),N=(0,d.useCallback)((e={},t=null)=>({id:f,...e,ref:(0,r.lq)(t,e=>{e&&x(!0)}),"aria-live":"polite"}),[f]),k=(0,d.useCallback)((e={},t=null)=>({...e,...s,ref:t,role:"group","data-focus":(0,c.PB)(g),"data-disabled":(0,c.PB)(i),"data-invalid":(0,c.PB)(l),"data-readonly":(0,c.PB)(a)}),[s,i,g,l,a]);return{isRequired:!!n,isInvalid:!!l,isReadOnly:!!a,isDisabled:!!i,isFocused:!!g,onFocus:()=>j(!0),onBlur:()=>j(!1),hasFeedbackText:h,setHasFeedbackText:x,hasHelpText:v,setHasHelpText:b,id:u,labelId:m,feedbackId:f,helpTextId:p,htmlProps:s,getHelpTextProps:y,getErrorMessageProps:N,getRootProps:k,getLabelProps:_,getRequiredIndicatorProps:(0,d.useCallback)((e={},t=null)=>({...e,ref:t,role:"presentation","aria-hidden":!0,children:e.children||"*"}),[])}}((0,s.Lr)(e)),h=(0,c.cx)("chakra-form-control",e.className);return(0,u.jsx)(p,{value:f,children:(0,u.jsx)(m,{value:n,children:(0,u.jsx)(o.m.div,{...l({},t),className:h,__css:n.container})})})});x.displayName="FormControl",(0,i.G)(function(e,t){let n=h(),l=f(),r=(0,c.cx)("chakra-form__helper-text",e.className);return(0,u.jsx)(o.m.div,{...null==n?void 0:n.getHelpTextProps(e,t),__css:l.helperText,className:r})}).displayName="FormHelperText"},26621:function(e,t,n){n.d(t,{k:function(){return a}});var l=n(58250),r=n(82184),i=n(57437),a=(0,l.G)(function(e,t){let{direction:n,align:l,justify:a,wrap:s,basis:o,grow:c,shrink:d,...u}=e;return(0,i.jsx)(r.m.div,{ref:t,__css:{display:"flex",flexDirection:n,alignItems:l,justifyContent:a,flexWrap:s,flexBasis:o,flexGrow:c,flexShrink:d},...u})});a.displayName="Flex"},45663:function(e,t,n){n.d(t,{lq:function(){return r},qq:function(){return i}});var l=n(2265);function r(...e){return t=>{e.forEach(e=>{!function(e,t){if(null!=e){if("function"==typeof e){e(t);return}try{e.current=t}catch(n){throw Error(`Cannot assign value '${t}' to ref '${e}'`)}}}(e,t)})}}function i(...e){return(0,l.useMemo)(()=>r(...e),e)}},56641:function(e,t,n){n.d(t,{P:function(){return m}});var l=n(16465),r=n(58250),i=n(82184),a=n(57437),s=(0,r.G)(function(e,t){let{children:n,placeholder:r,className:s,...o}=e;return(0,a.jsxs)(i.m.select,{...o,ref:t,className:(0,l.cx)("chakra-select",s),children:[r&&(0,a.jsx)("option",{value:"",children:r}),n]})});s.displayName="SelectField";var o=n(6036),c=n(89839),d=n(50446),u=n(2265),m=(0,r.G)((e,t)=>{var n;let r=(0,c.jC)("Select",e),{rootProps:u,placeholder:m,icon:f,color:p,height:x,h:v,minH:b,minHeight:g,iconColor:j,iconSize:y,..._}=(0,d.Lr)(e),[N,k]=function(e,t){let n={},l={};for(let[r,i]of Object.entries(e))t.includes(r)?n[r]=i:l[r]=i;return[n,l]}(_,d.oE),w=(0,o.Y)(k),C={paddingEnd:"2rem",...r.field,_focus:{zIndex:"unset",...null==(n=r.field)?void 0:n._focus}};return(0,a.jsxs)(i.m.div,{className:"chakra-select__wrapper",__css:{width:"100%",height:"fit-content",position:"relative",color:p},...N,...u,children:[(0,a.jsx)(s,{ref:t,height:null!=v?v:x,minH:null!=b?b:g,placeholder:m,...w,__css:C,children:e.children}),(0,a.jsx)(h,{"data-disabled":(0,l.PB)(w.disabled),...(j||p)&&{color:j||p},__css:r.icon,...y&&{fontSize:y},children:f})]})});m.displayName="Select";var f=e=>(0,a.jsx)("svg",{viewBox:"0 0 24 24",...e,children:(0,a.jsx)("path",{fill:"currentColor",d:"M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"})}),p=(0,i.m)("div",{baseStyle:{position:"absolute",display:"inline-flex",alignItems:"center",justifyContent:"center",pointerEvents:"none",top:"50%",transform:"translateY(-50%)"}}),h=e=>{let{children:t=(0,a.jsx)(f,{}),...n}=e,l=(0,u.cloneElement)(t,{role:"presentation",className:"chakra-select__icon",focusable:!1,"aria-hidden":!0,style:{width:"1em",height:"1em",color:"currentColor"}});return(0,a.jsx)(p,{...n,className:"chakra-select__icon-wrapper",children:(0,u.isValidElement)(t)?l:null})};h.displayName="SelectIcon"},73623:function(e,t,n){n.d(t,{p:function(){return s}});var l=n(6161),r=n(8936),i=n(12704),a=n(2265);function s(e){let{theme:t}=(0,i.uP)(),n=(0,l.OX)();return(0,a.useMemo)(()=>(0,r.Cj)(t.direction,{...n,...e}),[e,t.direction,n])}}}]);