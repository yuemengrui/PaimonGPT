"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[112],{10369:function(t,e,r){r.d(e,{a:function(){return n}});var a=r(66732);function n(t,e){var r=t.append("foreignObject").attr("width","100000"),n=r.append("xhtml:div");n.attr("xmlns","http://www.w3.org/1999/xhtml");var l=e.label;switch(typeof l){case"function":n.insert(l);break;case"object":n.insert(function(){return l});break;default:n.html(l)}a.bg(n,e.labelStyle),n.style("display","inline-block"),n.style("white-space","nowrap");var i=n.node().getBoundingClientRect();return r.attr("width",i.width).attr("height",i.height),r}},66732:function(t,e,r){r.d(e,{$p:function(){return c},O1:function(){return i},WR:function(){return h},bF:function(){return l},bg:function(){return d}});var a=r(49227),n=r(85491);function l(t,e){return!!t.children(e).length}function i(t){return s(t.v)+":"+s(t.w)+":"+s(t.name)}var o=/:/g;function s(t){return t?String(t).replace(o,"\\:"):""}function d(t,e){e&&t.attr("style",e)}function c(t,e,r){e&&t.attr("class",e).attr("class",r+" "+t.attr("class"))}function h(t,e){var r=e.graph();if(a.Z(r)){var l=r.transition;if(n.Z(l))return l(t)}return t}},61649:function(t,e,r){var a=r(17169),n=r(76496);e.Z=(t,e)=>a.Z.lang.round(n.Z.parse(t)[e])},40112:function(t,e,r){r.d(e,{diagram:function(){return Q}});var a=r(52517),n=r(17928),l=r(29868),i=r(82466),o=r(91067),s=r(74683),d=r(10790),c=r(35855),h=r(66732),u={normal:function(t,e,r,a){var n=t.append("marker").attr("id",e).attr("viewBox","0 0 10 10").attr("refX",9).attr("refY",5).attr("markerUnits","strokeWidth").attr("markerWidth",8).attr("markerHeight",6).attr("orient","auto").append("path").attr("d","M 0 0 L 10 5 L 0 10 z").style("stroke-width",1).style("stroke-dasharray","1,0");h.bg(n,r[a+"Style"]),r[a+"Class"]&&n.attr("class",r[a+"Class"])},vee:function(t,e,r,a){var n=t.append("marker").attr("id",e).attr("viewBox","0 0 10 10").attr("refX",9).attr("refY",5).attr("markerUnits","strokeWidth").attr("markerWidth",8).attr("markerHeight",6).attr("orient","auto").append("path").attr("d","M 0 0 L 10 5 L 0 10 L 4 5 z").style("stroke-width",1).style("stroke-dasharray","1,0");h.bg(n,r[a+"Style"]),r[a+"Class"]&&n.attr("class",r[a+"Class"])},undirected:function(t,e,r,a){var n=t.append("marker").attr("id",e).attr("viewBox","0 0 10 10").attr("refX",9).attr("refY",5).attr("markerUnits","strokeWidth").attr("markerWidth",8).attr("markerHeight",6).attr("orient","auto").append("path").attr("d","M 0 5 L 10 5").style("stroke-width",1).style("stroke-dasharray","1,0");h.bg(n,r[a+"Style"]),r[a+"Class"]&&n.attr("class",r[a+"Class"])}},p=r(10369);function f(t,e,r){var a,n=e.label,l=t.append("g");"svg"===e.labelType?(l.node().appendChild(e.label),h.bg(l,e.labelStyle)):"string"!=typeof n||"html"===e.labelType?(0,p.a)(l,e):function(t,e){for(var r=t.append("text"),a=(function(t){for(var e,r="",a=!1,n=0;n<t.length;++n)(e=t[n],a)?("n"===e?r+="\n":r+=e,a=!1):"\\"===e?a=!0:r+=e;return r})(e.label).split("\n"),n=0;n<a.length;n++)r.append("tspan").attr("xml:space","preserve").attr("dy","1em").attr("x","1").text(a[n]);return h.bg(r,e.labelStyle),r}(l,e);var i=l.node().getBBox();switch(r){case"top":a=-e.height/2;break;case"bottom":a=e.height/2-i.height;break;default:a=-i.height/2}return l.attr("transform","translate("+-i.width/2+","+a+")"),l}var g=function(t,e){var r=e.nodes().filter(function(t){return h.bF(e,t)}),a=t.selectAll("g.cluster").data(r,function(t){return t});h.WR(a.exit(),e).style("opacity",0).remove();var n=a.enter().append("g").attr("class","cluster").attr("id",function(t){return e.node(t).id}).style("opacity",0).each(function(t){var r=e.node(t),a=l.Ys(this);l.Ys(this).append("rect"),f(a.append("g").attr("class","label"),r,r.clusterLabelPos)});return a=a.merge(n),(a=h.WR(a,e).style("opacity",1)).selectAll("rect").each(function(t){var r=e.node(t),a=l.Ys(this);h.bg(a,r.style)}),a};let y=function(t,e){var r,a=t.selectAll("g.edgeLabel").data(e.edges(),function(t){return h.O1(t)}).classed("update",!0);return a.exit().remove(),a.enter().append("g").classed("edgeLabel",!0).style("opacity",0),(a=t.selectAll("g.edgeLabel")).each(function(t){var r=l.Ys(this);r.select(".label").remove();var a=e.edge(t),n=f(r,e.edge(t),0).classed("label",!0),i=n.node().getBBox();a.labelId&&n.attr("id",a.labelId),o.Z(a,"width")||(a.width=i.width),o.Z(a,"height")||(a.height=i.height)}),r=a.exit?a.exit():a.selectAll(null),h.WR(r,e).style("opacity",0).remove(),a};var b=r(65544),w=r(32648);function x(t,e){return t.intersect(e)}var v=function(t,e,r){var a,n=t.selectAll("g.edgePath").data(e.edges(),function(t){return h.O1(t)}).classed("update",!0),i=((a=n.enter().append("g").attr("class","edgePath").style("opacity",0)).append("path").attr("class","path").attr("d",function(t){var r=e.edge(t),a=e.node(t.v).elem,n=w.Z(r.points.length).map(function(){var t,e;return t=a.getBBox(),{x:(e=a.ownerSVGElement.getScreenCTM().inverse().multiply(a.getScreenCTM()).translate(t.width/2,t.height/2)).e,y:e.f}});return k(r,n)}),a.append("defs"),a);!function(t,e){var r=t.exit();h.WR(r,e).style("opacity",0).remove()}(n,e);var o=void 0!==n.merge?n.merge(i):n;return h.WR(o,e).style("opacity",1),o.each(function(t){var r=l.Ys(this),a=e.edge(t);a.elem=this,a.id&&r.attr("id",a.id),h.$p(r,a.class,(r.classed("update")?"update ":"")+"edgePath")}),o.selectAll("path.path").each(function(t){var r=e.edge(t);r.arrowheadId=b.Z("arrowhead");var a=l.Ys(this).attr("marker-end",function(){var t,e;return"url("+(t=location.href,e=r.arrowheadId,t.split("#")[0]+"#"+e)+")"}).style("fill","none");h.WR(a,e).attr("d",function(t){var r,a,n,l;return r=e.edge(t),a=e.node(t.v),n=e.node(t.w),(l=r.points.slice(1,r.points.length-1)).unshift(x(a,l[0])),l.push(x(n,l[l.length-1])),k(r,l)}),h.bg(a,r.style)}),o.selectAll("defs *").remove(),o.selectAll("defs").each(function(t){var a=e.edge(t);(0,r[a.arrowhead])(l.Ys(this),a.arrowheadId,a,"arrowhead")}),o};function k(t,e){var r=(l.jvg||l.YPS.line)().x(function(t){return t.x}).y(function(t){return t.y});return(r.curve||r.interpolate)(t.curve),r(e)}var m=r(50004),S=function(t,e,r){var a,n=e.nodes().filter(function(t){return!h.bF(e,t)}),i=t.selectAll("g.node").data(n,function(t){return t}).classed("update",!0);return i.exit().remove(),i.enter().append("g").attr("class","node").style("opacity",0),(i=t.selectAll("g.node")).each(function(t){var a=e.node(t),n=l.Ys(this);h.$p(n,a.class,(n.classed("update")?"update ":"")+"node"),n.select("g.label").remove();var i=n.append("g").attr("class","label"),s=f(i,a),d=r[a.shape],c=m.Z(s.node().getBBox(),"width","height");a.elem=this,a.id&&n.attr("id",a.id),a.labelId&&i.attr("id",a.labelId),o.Z(a,"width")&&(c.width=a.width),o.Z(a,"height")&&(c.height=a.height),c.width+=a.paddingLeft+a.paddingRight,c.height+=a.paddingTop+a.paddingBottom,i.attr("transform","translate("+(a.paddingLeft-a.paddingRight)/2+","+(a.paddingTop-a.paddingBottom)/2+")");var u=l.Ys(this);u.select(".label-container").remove();var p=d(u,c,a).classed("label-container",!0);h.bg(p,a.style);var g=p.node().getBBox();a.width=g.width,a.height=g.height}),a=i.exit?i.exit():i.selectAll(null),h.WR(a,e).style("opacity",0).remove(),i};function _(t,e,r,a){var n=t.x,l=t.y,i=n-a.x,o=l-a.y,s=Math.sqrt(e*e*o*o+r*r*i*i),d=Math.abs(e*r*i/s);a.x<n&&(d=-d);var c=Math.abs(e*r*o/s);return a.y<l&&(c=-c),{x:n+d,y:l+c}}function T(t,e,r){var a=t.x,n=t.y,l=[],i=Number.POSITIVE_INFINITY,o=Number.POSITIVE_INFINITY;e.forEach(function(t){i=Math.min(i,t.x),o=Math.min(o,t.y)});for(var s=a-t.width/2-i,d=n-t.height/2-o,c=0;c<e.length;c++){var h=e[c],u=e[c<e.length-1?c+1:0],p=function(t,e,r,a){var n,l,i,o,s,d,c,h,u,p,f,g,y;if(n=e.y-t.y,i=t.x-e.x,s=e.x*t.y-t.x*e.y,u=n*r.x+i*r.y+s,p=n*a.x+i*a.y+s,(0===u||0===p||!(u*p>0))&&(l=a.y-r.y,o=r.x-a.x,d=a.x*r.y-r.x*a.y,c=l*t.x+o*t.y+d,h=l*e.x+o*e.y+d,!(0!==c&&0!==h&&c*h>0)&&0!=(f=n*o-l*i)))return g=Math.abs(f/2),{x:(y=i*d-o*s)<0?(y-g)/f:(y+g)/f,y:(y=l*s-n*d)<0?(y-g)/f:(y+g)/f}}(t,r,{x:s+h.x,y:d+h.y},{x:s+u.x,y:d+u.y});p&&l.push(p)}return l.length?(l.length>1&&l.sort(function(t,e){var a=t.x-r.x,n=t.y-r.y,l=Math.sqrt(a*a+n*n),i=e.x-r.x,o=e.y-r.y,s=Math.sqrt(i*i+o*o);return l<s?-1:l===s?0:1}),l[0]):(console.log("NO INTERSECTION FOUND, RETURN NODE CENTER",t),t)}function L(t,e){var r,a,n=t.x,l=t.y,i=e.x-n,o=e.y-l,s=t.width/2,d=t.height/2;return Math.abs(o)*s>Math.abs(i)*d?(o<0&&(d=-d),r=0===o?0:d*i/o,a=d):(i<0&&(s=-s),r=s,a=0===i?0:s*o/i),{x:n+r,y:l+a}}var C={rect:function(t,e,r){var a=t.insert("rect",":first-child").attr("rx",r.rx).attr("ry",r.ry).attr("x",-e.width/2).attr("y",-e.height/2).attr("width",e.width).attr("height",e.height);return r.intersect=function(t){return L(r,t)},a},ellipse:function(t,e,r){var a=e.width/2,n=e.height/2,l=t.insert("ellipse",":first-child").attr("x",-e.width/2).attr("y",-e.height/2).attr("rx",a).attr("ry",n);return r.intersect=function(t){return _(r,a,n,t)},l},circle:function(t,e,r){var a=Math.max(e.width,e.height)/2,n=t.insert("circle",":first-child").attr("x",-e.width/2).attr("y",-e.height/2).attr("r",a);return r.intersect=function(t){return _(r,a,a,t)},n},diamond:function(t,e,r){var a=e.width*Math.SQRT2/2,n=e.height*Math.SQRT2/2,l=[{x:0,y:-n},{x:-a,y:0},{x:0,y:n},{x:a,y:0}],i=t.insert("polygon",":first-child").attr("points",l.map(function(t){return t.x+","+t.y}).join(" "));return r.intersect=function(t){return T(r,l,t)},i}};function A(){var t=function(t,e){e.nodes().forEach(function(t){var r=e.node(t);o.Z(r,"label")||e.children(t).length||(r.label=t),o.Z(r,"paddingX")&&s.Z(r,{paddingLeft:r.paddingX,paddingRight:r.paddingX}),o.Z(r,"paddingY")&&s.Z(r,{paddingTop:r.paddingY,paddingBottom:r.paddingY}),o.Z(r,"padding")&&s.Z(r,{paddingLeft:r.padding,paddingRight:r.padding,paddingTop:r.padding,paddingBottom:r.padding}),s.Z(r,N),d.Z(["paddingLeft","paddingRight","paddingTop","paddingBottom"],function(t){r[t]=Number(r[t])}),o.Z(r,"width")&&(r._prevWidth=r.width),o.Z(r,"height")&&(r._prevHeight=r.height)}),e.edges().forEach(function(t){var r=e.edge(t);o.Z(r,"label")||(r.label=""),s.Z(r,B)});var r=$(t,"output"),a=$(r,"clusters"),n=$(r,"edgePaths"),i=y($(r,"edgeLabels"),e),p=S($(r,"nodes"),e,C);(0,c.bK)(e),function(t,e){function r(t){var r=e.node(t);return"translate("+r.x+","+r.y+")"}t.filter(function(){return!l.Ys(this).classed("update")}).attr("transform",r),h.WR(t,e).style("opacity",1).attr("transform",r)}(p,e),function(t,e){function r(t){var r=e.edge(t);return o.Z(r,"x")?"translate("+r.x+","+r.y+")":""}t.filter(function(){return!l.Ys(this).classed("update")}).attr("transform",r),h.WR(t,e).style("opacity",1).attr("transform",r)}(i,e),v(n,e,u),function(t,e){var r=t.filter(function(){return!l.Ys(this).classed("update")});function a(t){var r=e.node(t);return"translate("+r.x+","+r.y+")"}r.attr("transform",a),h.WR(t,e).style("opacity",1).attr("transform",a),h.WR(r.selectAll("rect"),e).attr("width",function(t){return e.node(t).width}).attr("height",function(t){return e.node(t).height}).attr("x",function(t){return-e.node(t).width/2}).attr("y",function(t){return-e.node(t).height/2})}(g(a,e),e),d.Z(e.nodes(),function(t){var r=e.node(t);o.Z(r,"_prevWidth")?r.width=r._prevWidth:delete r.width,o.Z(r,"_prevHeight")?r.height=r._prevHeight:delete r.height,delete r._prevWidth,delete r._prevHeight})};return t.createNodes=function(e){return arguments.length?(S=e,t):S},t.createClusters=function(e){return arguments.length?(g=e,t):g},t.createEdgeLabels=function(e){return arguments.length?(y=e,t):y},t.createEdgePaths=function(e){return arguments.length?(v=e,t):v},t.shapes=function(e){return arguments.length?(C=e,t):C},t.arrows=function(e){return arguments.length?(u=e,t):u},t}var N={paddingLeft:10,paddingRight:10,paddingTop:10,paddingBottom:10,rx:0,ry:0,shape:"rect"},B={arrowhead:"normal",curve:l.c_6};function $(t,e){var r=t.select("g."+e);return r.empty()&&(r=t.append("g").attr("class",e)),r}var E=r(45440);function I(t,e,r){let a=(e.width+e.height)*.9,n=[{x:a/2,y:0},{x:a,y:-a/2},{x:a/2,y:-a},{x:0,y:-a/2}],l=j(t,a,a,n);return r.intersect=function(t){return T(r,n,t)},l}function M(t,e,r){let a=e.height,n=a/4,l=e.width+2*n,i=[{x:n,y:0},{x:l-n,y:0},{x:l,y:-a/2},{x:l-n,y:-a},{x:n,y:-a},{x:0,y:-a/2}],o=j(t,l,a,i);return r.intersect=function(t){return T(r,i,t)},o}function R(t,e,r){let a=e.width,n=e.height,l=[{x:-n/2,y:0},{x:a,y:0},{x:a,y:-n},{x:-n/2,y:-n},{x:0,y:-n/2}],i=j(t,a,n,l);return r.intersect=function(t){return T(r,l,t)},i}function Y(t,e,r){let a=e.width,n=e.height,l=[{x:-2*n/6,y:0},{x:a-n/6,y:0},{x:a+2*n/6,y:-n},{x:n/6,y:-n}],i=j(t,a,n,l);return r.intersect=function(t){return T(r,l,t)},i}function Z(t,e,r){let a=e.width,n=e.height,l=[{x:2*n/6,y:0},{x:a+n/6,y:0},{x:a-2*n/6,y:-n},{x:-n/6,y:-n}],i=j(t,a,n,l);return r.intersect=function(t){return T(r,l,t)},i}function D(t,e,r){let a=e.width,n=e.height,l=[{x:-2*n/6,y:0},{x:a+2*n/6,y:0},{x:a-n/6,y:-n},{x:n/6,y:-n}],i=j(t,a,n,l);return r.intersect=function(t){return T(r,l,t)},i}function W(t,e,r){let a=e.width,n=e.height,l=[{x:n/6,y:0},{x:a-n/6,y:0},{x:a+2*n/6,y:-n},{x:-2*n/6,y:-n}],i=j(t,a,n,l);return r.intersect=function(t){return T(r,l,t)},i}function U(t,e,r){let a=e.width,n=e.height,l=[{x:0,y:0},{x:a+n/2,y:0},{x:a,y:-n/2},{x:a+n/2,y:-n},{x:0,y:-n}],i=j(t,a,n,l);return r.intersect=function(t){return T(r,l,t)},i}function z(t,e,r){let a=e.height,n=e.width+a/4,l=t.insert("rect",":first-child").attr("rx",a/2).attr("ry",a/2).attr("x",-n/2).attr("y",-a/2).attr("width",n).attr("height",a);return r.intersect=function(t){return L(r,t)},l}function O(t,e,r){let a=e.width,n=e.height,l=[{x:0,y:0},{x:a,y:0},{x:a,y:-n},{x:0,y:-n},{x:0,y:0},{x:-8,y:0},{x:a+8,y:0},{x:a+8,y:-n},{x:-8,y:-n},{x:-8,y:0}],i=j(t,a,n,l);return r.intersect=function(t){return T(r,l,t)},i}function P(t,e,r){let a=e.width,n=a/2,l=n/(2.5+a/50),i=e.height+l,o=t.attr("label-offset-y",l).insert("path",":first-child").attr("d","M 0,"+l+" a "+n+","+l+" 0,0,0 "+a+" 0 a "+n+","+l+" 0,0,0 "+-a+" 0 l 0,"+i+" a "+n+","+l+" 0,0,0 "+a+" 0 l 0,"+-i).attr("transform","translate("+-a/2+","+-(i/2+l)+")");return r.intersect=function(t){let e=L(r,t),a=e.x-r.x;if(0!=n&&(Math.abs(a)<r.width/2||Math.abs(a)==r.width/2&&Math.abs(e.y-r.y)>r.height/2-l)){let i=l*l*(1-a*a/(n*n));0!=i&&(i=Math.sqrt(i)),i=l-i,t.y-r.y>0&&(i=-i),e.y+=i}return e},o}function j(t,e,r,a){return t.insert("polygon",":first-child").attr("points",a.map(function(t){return t.x+","+t.y}).join(" ")).attr("transform","translate("+-e/2+","+r/2+")")}r(74548),r(41417),r(43571),r(79160);let q={addToRender:function(t){t.shapes().question=I,t.shapes().hexagon=M,t.shapes().stadium=z,t.shapes().subroutine=O,t.shapes().cylinder=P,t.shapes().rect_left_inv_arrow=R,t.shapes().lean_right=Y,t.shapes().lean_left=Z,t.shapes().trapezoid=D,t.shapes().inv_trapezoid=W,t.shapes().rect_right_inv_arrow=U},addToRenderV2:function(t){t({question:I}),t({hexagon:M}),t({stadium:z}),t({subroutine:O}),t({cylinder:P}),t({rect_left_inv_arrow:R}),t({lean_right:Y}),t({lean_left:Z}),t({trapezoid:D}),t({inv_trapezoid:W}),t({rect_right_inv_arrow:U})}},V={},X=async function(t,e,r,a,n,o){let s=a?a.select(`[id="${r}"]`):(0,l.Ys)(`[id="${r}"]`),d=n||document;for(let r of Object.keys(t)){let a;let n=t[r],l="default";n.classes.length>0&&(l=n.classes.join(" "));let c=(0,i.k)(n.styles),h=void 0!==n.text?n.text:n.id;if((0,i.m)((0,i.c)().flowchart.htmlLabels)){let t={label:await (0,i.r)(h.replace(/fa[blrs]?:fa-[\w-]+/g,t=>`<i class='${t.replace(":"," ")}'></i>`),(0,i.c)())};(a=(0,p.a)(s,t).node()).parentNode.removeChild(a)}else{let t=d.createElementNS("http://www.w3.org/2000/svg","text");for(let e of(t.setAttribute("style",c.labelStyle.replace("color:","fill:")),h.split(i.e.lineBreakRegex))){let r=d.createElementNS("http://www.w3.org/2000/svg","tspan");r.setAttributeNS("http://www.w3.org/XML/1998/namespace","xml:space","preserve"),r.setAttribute("dy","1em"),r.setAttribute("x","1"),r.textContent=e,t.appendChild(r)}a=t}let u=0,f="";switch(n.type){case"round":u=5,f="rect";break;case"square":case"group":default:f="rect";break;case"diamond":f="question";break;case"hexagon":f="hexagon";break;case"odd":case"odd_right":f="rect_left_inv_arrow";break;case"lean_right":f="lean_right";break;case"lean_left":f="lean_left";break;case"trapezoid":f="trapezoid";break;case"inv_trapezoid":f="inv_trapezoid";break;case"circle":f="circle";break;case"ellipse":f="ellipse";break;case"stadium":f="stadium";break;case"subroutine":f="subroutine";break;case"cylinder":f="cylinder"}i.l.warn("Adding node",n.id,n.domId),e.setNode(o.db.lookUpDomId(n.id),{labelType:"svg",labelStyle:c.labelStyle,shape:f,label:a,rx:u,ry:u,class:l,style:c.style,id:o.db.lookUpDomId(n.id)})}},F=async function(t,e,r){let a,n,o=0;if(void 0!==t.defaultStyle){let e=(0,i.k)(t.defaultStyle);a=e.style,n=e.labelStyle}for(let s of t){o++;let d="L-"+s.start+"-"+s.end,c="LS-"+s.start,h="LE-"+s.end,u={};"arrow_open"===s.type?u.arrowhead="none":u.arrowhead="normal";let p="",f="";if(void 0!==s.style){let t=(0,i.k)(s.style);p=t.style,f=t.labelStyle}else switch(s.stroke){case"normal":p="fill:none",void 0!==a&&(p=a),void 0!==n&&(f=n);break;case"dotted":p="fill:none;stroke-width:2px;stroke-dasharray:3;";break;case"thick":p=" stroke-width: 3.5px;fill:none"}u.style=p,u.labelStyle=f,void 0!==s.interpolate?u.curve=(0,i.n)(s.interpolate,l.c_6):void 0!==t.defaultInterpolate?u.curve=(0,i.n)(t.defaultInterpolate,l.c_6):u.curve=(0,i.n)(V.curve,l.c_6),void 0===s.text?void 0!==s.style&&(u.arrowheadStyle="fill: #333"):(u.arrowheadStyle="fill: #333",u.labelpos="c",(0,i.m)((0,i.c)().flowchart.htmlLabels)?(u.labelType="html",u.label=`<span id="L-${d}" class="edgeLabel L-${c}' L-${h}" style="${u.labelStyle}">${await (0,i.r)(s.text.replace(/fa[blrs]?:fa-[\w-]+/g,t=>`<i class='${t.replace(":"," ")}'></i>`),(0,i.c)())}</span>`):(u.labelType="text",u.label=s.text.replace(i.e.lineBreakRegex,"\n"),void 0===s.style&&(u.style=u.style||"stroke: #333; stroke-width: 1.5px;fill:none"),u.labelStyle=u.labelStyle.replace("color:","fill:"))),u.id=d,u.class=c+" "+h,u.minlen=s.length||1,e.setEdge(r.db.lookUpDomId(s.start),r.db.lookUpDomId(s.end),u,o)}},G=async function(t,e,r,a){let o,s;i.l.info("Drawing flowchart");let{securityLevel:d,flowchart:c}=(0,i.c)();"sandbox"===d&&(o=(0,l.Ys)("#i"+e));let u="sandbox"===d?(0,l.Ys)(o.nodes()[0].contentDocument.body):(0,l.Ys)("body"),p="sandbox"===d?o.nodes()[0].contentDocument:document,f=a.db.getDirection();void 0===f&&(f="TD");let g=c.nodeSpacing||50,y=c.rankSpacing||50,b=new n.k({multigraph:!0,compound:!0}).setGraph({rankdir:f,nodesep:g,ranksep:y,marginx:8,marginy:8}).setDefaultEdgeLabel(function(){return{}}),w=a.db.getSubGraphs();for(let t=w.length-1;t>=0;t--)s=w[t],a.db.addVertex(s.id,s.title,"group",void 0,s.classes);let x=a.db.getVertices();i.l.warn("Get vertices",x);let v=a.db.getEdges(),k=0;for(k=w.length-1;k>=0;k--){s=w[k],(0,l.td_)("cluster").append("text");for(let t=0;t<s.nodes.length;t++)i.l.warn("Setting subgraph",s.nodes[t],a.db.lookUpDomId(s.nodes[t]),a.db.lookUpDomId(s.id)),b.setParent(a.db.lookUpDomId(s.nodes[t]),a.db.lookUpDomId(s.id))}await X(x,b,e,u,p,a),await F(v,b,a);let m=new A;q.addToRender(m),m.arrows().none=function(t,e,r,a){let n=t.append("marker").attr("id",e).attr("viewBox","0 0 10 10").attr("refX",9).attr("refY",5).attr("markerUnits","strokeWidth").attr("markerWidth",8).attr("markerHeight",6).attr("orient","auto").append("path").attr("d","M 0 0 L 0 0 L 0 0 z");(0,h.bg)(n,r[a+"Style"])},m.arrows().normal=function(t,e){t.append("marker").attr("id",e).attr("viewBox","0 0 10 10").attr("refX",9).attr("refY",5).attr("markerUnits","strokeWidth").attr("markerWidth",8).attr("markerHeight",6).attr("orient","auto").append("path").attr("d","M 0 0 L 10 5 L 0 10 z").attr("class","arrowheadPath").style("stroke-width",1).style("stroke-dasharray","1,0")};let S=u.select(`[id="${e}"]`),_=u.select("#"+e+" g");for(m(_,b),_.selectAll("g.node").attr("title",function(){return a.db.getTooltip(this.id)}),a.db.indexNodes("subGraph"+k),k=0;k<w.length;k++)if("undefined"!==(s=w[k]).title){let t=p.querySelectorAll("#"+e+' [id="'+a.db.lookUpDomId(s.id)+'"] rect'),r=p.querySelectorAll("#"+e+' [id="'+a.db.lookUpDomId(s.id)+'"]'),n=t[0].x.baseVal.value,i=t[0].y.baseVal.value,o=t[0].width.baseVal.value,d=(0,l.Ys)(r[0]).select(".label");d.attr("transform",`translate(${n+o/2}, ${i+14})`),d.attr("id",e+"Text");for(let t=0;t<s.classes.length;t++)r[0].classList.add(s.classes[t])}if(!c.htmlLabels)for(let t of p.querySelectorAll('[id="'+e+'"] .edgeLabel .label')){let e=t.getBBox(),r=p.createElementNS("http://www.w3.org/2000/svg","rect");r.setAttribute("rx",0),r.setAttribute("ry",0),r.setAttribute("width",e.width),r.setAttribute("height",e.height),t.insertBefore(r,t.firstChild)}(0,i.o)(b,S,c.diagramPadding,c.useMaxWidth),Object.keys(x).forEach(function(t){let r=x[t];if(r.link){let n=u.select("#"+e+' [id="'+a.db.lookUpDomId(t)+'"]');if(n){let t=p.createElementNS("http://www.w3.org/2000/svg","a");t.setAttributeNS("http://www.w3.org/2000/svg","class",r.classes.join(" ")),t.setAttributeNS("http://www.w3.org/2000/svg","href",r.link),t.setAttributeNS("http://www.w3.org/2000/svg","rel","noopener"),"sandbox"===d?t.setAttributeNS("http://www.w3.org/2000/svg","target","_top"):r.linkTarget&&t.setAttributeNS("http://www.w3.org/2000/svg","target",r.linkTarget);let e=n.insert(function(){return t},":first-child"),a=n.select(".label-container");a&&e.append(function(){return a.node()});let l=n.select(".label");l&&e.append(function(){return l.node()})}}})},H={setConf:function(t){for(let e of Object.keys(t))V[e]=t[e]},addVertices:X,addEdges:F,getClasses:function(t,e){return i.l.info("Extracting classes"),e.db.getClasses()},draw:G},Q={parser:a.p,db:a.f,renderer:E.f,styles:E.a,init:t=>{t.flowchart||(t.flowchart={}),t.flowchart.arrowMarkerAbsolute=t.arrowMarkerAbsolute,H.setConf(t.flowchart),a.f.clear(),a.f.setGen("gen-1")}}},45440:function(t,e,r){r.d(e,{a:function(){return y},f:function(){return f}});var a=r(17928),n=r(29868),l=r(82466),i=r(92876),o=r(10369),s=r(61649),d=r(64369);let c={},h=async function(t,e,r,a,n,i){let s=a.select(`[id="${r}"]`);for(let r of Object.keys(t)){let a;let d=t[r],c="default";d.classes.length>0&&(c=d.classes.join(" ")),c+=" flowchart-label";let h=(0,l.k)(d.styles),u=void 0!==d.text?d.text:d.id;if(l.l.info("vertex",d,d.labelType),"markdown"===d.labelType)l.l.info("vertex",d,d.labelType);else if((0,l.m)((0,l.c)().flowchart.htmlLabels)){let t={label:u};(a=(0,o.a)(s,t).node()).parentNode.removeChild(a)}else{let t=n.createElementNS("http://www.w3.org/2000/svg","text");for(let e of(t.setAttribute("style",h.labelStyle.replace("color:","fill:")),u.split(l.e.lineBreakRegex))){let r=n.createElementNS("http://www.w3.org/2000/svg","tspan");r.setAttributeNS("http://www.w3.org/XML/1998/namespace","xml:space","preserve"),r.setAttribute("dy","1em"),r.setAttribute("x","1"),r.textContent=e,t.appendChild(r)}a=t}let p=0,f="";switch(d.type){case"round":p=5,f="rect";break;case"square":case"group":default:f="rect";break;case"diamond":f="question";break;case"hexagon":f="hexagon";break;case"odd":case"odd_right":f="rect_left_inv_arrow";break;case"lean_right":f="lean_right";break;case"lean_left":f="lean_left";break;case"trapezoid":f="trapezoid";break;case"inv_trapezoid":f="inv_trapezoid";break;case"circle":f="circle";break;case"ellipse":f="ellipse";break;case"stadium":f="stadium";break;case"subroutine":f="subroutine";break;case"cylinder":f="cylinder";break;case"doublecircle":f="doublecircle"}let g=await (0,l.r)(u,(0,l.c)());e.setNode(d.id,{labelStyle:h.labelStyle,shape:f,labelText:g,labelType:d.labelType,rx:p,ry:p,class:c,style:h.style,id:d.id,link:d.link,linkTarget:d.linkTarget,tooltip:i.db.getTooltip(d.id)||"",domId:i.db.lookUpDomId(d.id),haveCallback:d.haveCallback,width:"group"===d.type?500:void 0,dir:d.dir,type:d.type,props:d.props,padding:(0,l.c)().flowchart.padding}),l.l.info("setNode",{labelStyle:h.labelStyle,labelType:d.labelType,shape:f,labelText:g,rx:p,ry:p,class:c,style:h.style,id:d.id,domId:i.db.lookUpDomId(d.id),width:"group"===d.type?500:void 0,type:d.type,dir:d.dir,props:d.props,padding:(0,l.c)().flowchart.padding})}},u=async function(t,e,r){let a,i;l.l.info("abc78 edges = ",t);let o=0,s={};if(void 0!==t.defaultStyle){let e=(0,l.k)(t.defaultStyle);a=e.style,i=e.labelStyle}for(let r of t){o++;let d="L-"+r.start+"-"+r.end;void 0===s[d]?s[d]=0:s[d]++,l.l.info("abc78 new entry",d,s[d]);let h=d+"-"+s[d];l.l.info("abc78 new link id to be used is",d,h,s[d]);let u="LS-"+r.start,p="LE-"+r.end,f={style:"",labelStyle:""};switch(f.minlen=r.length||1,"arrow_open"===r.type?f.arrowhead="none":f.arrowhead="normal",f.arrowTypeStart="arrow_open",f.arrowTypeEnd="arrow_open",r.type){case"double_arrow_cross":f.arrowTypeStart="arrow_cross";case"arrow_cross":f.arrowTypeEnd="arrow_cross";break;case"double_arrow_point":f.arrowTypeStart="arrow_point";case"arrow_point":f.arrowTypeEnd="arrow_point";break;case"double_arrow_circle":f.arrowTypeStart="arrow_circle";case"arrow_circle":f.arrowTypeEnd="arrow_circle"}let g="",y="";switch(r.stroke){case"normal":g="fill:none;",void 0!==a&&(g=a),void 0!==i&&(y=i),f.thickness="normal",f.pattern="solid";break;case"dotted":f.thickness="normal",f.pattern="dotted",f.style="fill:none;stroke-width:2px;stroke-dasharray:3;";break;case"thick":f.thickness="thick",f.pattern="solid",f.style="stroke-width: 3.5px;fill:none;";break;case"invisible":f.thickness="invisible",f.pattern="solid",f.style="stroke-width: 0;fill:none;"}if(void 0!==r.style){let t=(0,l.k)(r.style);g=t.style,y=t.labelStyle}f.style=f.style+=g,f.labelStyle=f.labelStyle+=y,void 0!==r.interpolate?f.curve=(0,l.n)(r.interpolate,n.c_6):void 0!==t.defaultInterpolate?f.curve=(0,l.n)(t.defaultInterpolate,n.c_6):f.curve=(0,l.n)(c.curve,n.c_6),void 0===r.text?void 0!==r.style&&(f.arrowheadStyle="fill: #333"):(f.arrowheadStyle="fill: #333",f.labelpos="c"),f.labelType=r.labelType,f.label=await (0,l.r)(r.text.replace(l.e.lineBreakRegex,"\n"),(0,l.c)()),void 0===r.style&&(f.style=f.style||"stroke: #333; stroke-width: 1.5px;fill:none;"),f.labelStyle=f.labelStyle.replace("color:","fill:"),f.id=h,f.classes="flowchart-link "+u+" "+p,e.setEdge(r.start,r.end,f,o)}},p=async function(t,e,r,o){let s,d;l.l.info("Drawing flowchart");let c=o.db.getDirection();void 0===c&&(c="TD");let{securityLevel:p,flowchart:f}=(0,l.c)(),g=f.nodeSpacing||50,y=f.rankSpacing||50;"sandbox"===p&&(s=(0,n.Ys)("#i"+e));let b="sandbox"===p?(0,n.Ys)(s.nodes()[0].contentDocument.body):(0,n.Ys)("body"),w="sandbox"===p?s.nodes()[0].contentDocument:document,x=new a.k({multigraph:!0,compound:!0}).setGraph({rankdir:c,nodesep:g,ranksep:y,marginx:0,marginy:0}).setDefaultEdgeLabel(function(){return{}}),v=o.db.getSubGraphs();l.l.info("Subgraphs - ",v);for(let t=v.length-1;t>=0;t--)d=v[t],l.l.info("Subgraph - ",d),o.db.addVertex(d.id,{text:d.title,type:d.labelType},"group",void 0,d.classes,d.dir);let k=o.db.getVertices(),m=o.db.getEdges();l.l.info("Edges",m);let S=0;for(S=v.length-1;S>=0;S--){d=v[S],(0,n.td_)("cluster").append("text");for(let t=0;t<d.nodes.length;t++)l.l.info("Setting up subgraphs",d.nodes[t],d.id),x.setParent(d.nodes[t],d.id)}await h(k,x,e,b,w,o),await u(m,x);let _=b.select(`[id="${e}"]`),T=b.select("#"+e+" g");if(await (0,i.r)(T,x,["point","circle","cross"],"flowchart",e),l.u.insertTitle(_,"flowchartTitleText",f.titleTopMargin,o.db.getDiagramTitle()),(0,l.o)(x,_,f.diagramPadding,f.useMaxWidth),o.db.indexNodes("subGraph"+S),!f.htmlLabels)for(let t of w.querySelectorAll('[id="'+e+'"] .edgeLabel .label')){let e=t.getBBox(),r=w.createElementNS("http://www.w3.org/2000/svg","rect");r.setAttribute("rx",0),r.setAttribute("ry",0),r.setAttribute("width",e.width),r.setAttribute("height",e.height),t.insertBefore(r,t.firstChild)}Object.keys(k).forEach(function(t){let r=k[t];if(r.link){let a=(0,n.Ys)("#"+e+' [id="'+t+'"]');if(a){let t=w.createElementNS("http://www.w3.org/2000/svg","a");t.setAttributeNS("http://www.w3.org/2000/svg","class",r.classes.join(" ")),t.setAttributeNS("http://www.w3.org/2000/svg","href",r.link),t.setAttributeNS("http://www.w3.org/2000/svg","rel","noopener"),"sandbox"===p?t.setAttributeNS("http://www.w3.org/2000/svg","target","_top"):r.linkTarget&&t.setAttributeNS("http://www.w3.org/2000/svg","target",r.linkTarget);let e=a.insert(function(){return t},":first-child"),n=a.select(".label-container");n&&e.append(function(){return n.node()});let l=a.select(".label");l&&e.append(function(){return l.node()})}}})},f={setConf:function(t){for(let e of Object.keys(t))c[e]=t[e]},addVertices:h,addEdges:u,getClasses:function(t,e){return e.db.getClasses()},draw:p},g=(t,e)=>{let r=s.Z,a=r(t,"r"),n=r(t,"g"),l=r(t,"b");return d.Z(a,n,l,e)},y=t=>`.label {
    font-family: ${t.fontFamily};
    color: ${t.nodeTextColor||t.textColor};
  }
  .cluster-label text {
    fill: ${t.titleColor};
  }
  .cluster-label span,p {
    color: ${t.titleColor};
  }

  .label text,span,p {
    fill: ${t.nodeTextColor||t.textColor};
    color: ${t.nodeTextColor||t.textColor};
  }

  .node rect,
  .node circle,
  .node ellipse,
  .node polygon,
  .node path {
    fill: ${t.mainBkg};
    stroke: ${t.nodeBorder};
    stroke-width: 1px;
  }
  .flowchart-label text {
    text-anchor: middle;
  }
  // .flowchart-label .text-outer-tspan {
  //   text-anchor: middle;
  // }
  // .flowchart-label .text-inner-tspan {
  //   text-anchor: start;
  // }

  .node .katex path {
    fill: #000;
    stroke: #000;
    stroke-width: 1px;
  }

  .node .label {
    text-align: center;
  }
  .node.clickable {
    cursor: pointer;
  }

  .arrowheadPath {
    fill: ${t.arrowheadColor};
  }

  .edgePath .path {
    stroke: ${t.lineColor};
    stroke-width: 2.0px;
  }

  .flowchart-link {
    stroke: ${t.lineColor};
    fill: none;
  }

  .edgeLabel {
    background-color: ${t.edgeLabelBackground};
    rect {
      opacity: 0.5;
      background-color: ${t.edgeLabelBackground};
      fill: ${t.edgeLabelBackground};
    }
    text-align: center;
  }

  /* For html labels only */
  .labelBkg {
    background-color: ${g(t.edgeLabelBackground,.5)};
    // background-color: 
  }

  .cluster rect {
    fill: ${t.clusterBkg};
    stroke: ${t.clusterBorder};
    stroke-width: 1px;
  }

  .cluster text {
    fill: ${t.titleColor};
  }

  .cluster span,p {
    color: ${t.titleColor};
  }
  /* .cluster div {
    color: ${t.titleColor};
  } */

  div.mermaidTooltip {
    position: absolute;
    text-align: center;
    max-width: 200px;
    padding: 2px;
    font-family: ${t.fontFamily};
    font-size: 12px;
    background: ${t.tertiaryColor};
    border: 1px solid ${t.border2};
    border-radius: 2px;
    pointer-events: none;
    z-index: 100;
  }

  .flowchartTitleText {
    text-anchor: middle;
    font-size: 18px;
    fill: ${t.textColor};
  }
`}}]);