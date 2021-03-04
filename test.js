const fs = require('fs');
const util = require('util');

let rawdata = fs.readFileSync('area.json');
let areas = JSON.parse(rawdata);

for (area in areas){
	let s = JSON.stringify(area);
	let sql = "insert into sys_area (id,parent_id,area_name,area_level,town_code) values('%s','%s','%s',%s,%s);\n"
	let data = areas[area]
	let r = util.format(sql, data.code, data.pcode,data.name,data.region_level,(!!data.type?"'"+data.type+"'":"null") )
	fs.appendFileSync('area.sql', r,(err)=>{throw err;})
}

