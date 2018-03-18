use std::fs::File;
use std::io::{BufReader,BufRead,Read};
use std::slice;

fn main() {
    let mut buffer: Vec<u8> = Vec::new();
    File::open("blockgroups.shp").unwrap().read_to_end(&mut buffer);


    let ids = BufReader::new(File::open("geoid.csv").unwrap()).lines().skip(1).map(|x| x.unwrap().chars().take(12).collect::<String>()).collect::<Vec<String>>();



    let size = 2 * unsafe { i32::from_be(*(buffer[24..28].as_ptr() as *const i32)) } as usize;
    let bbox = unsafe { *(buffer[36..68].as_ptr() as *const [f64; 4]) };

    println!("var geojson = {{ type: \"FeatureCollection\", bbox: {:?}, features: [", bbox);

    let mut idindex = 0;
    let mut offset = 100usize;
    while offset < size {
        let header = unsafe { *(buffer[offset..(offset+8)].as_ptr() as *const [i32; 2]) };
        let id = i32::from_be(header[0]);
        let len = 2 * i32::from_be(header[1]) as usize;

        offset += 8;

        let bbox = unsafe { *(buffer[(offset+4)..(offset+36)].as_ptr() as *const [f64; 4]) };
        let nparts  = unsafe { *(buffer[(offset+36)..(offset+40)].as_ptr() as *const i32) } as usize;
        let npoints = unsafe { *(buffer[(offset+40)..(offset+44)].as_ptr() as *const i32) } as usize;

        let i = offset + 44 + 4*nparts;
        let j = i + 16*npoints;
        let vertices = {
            let vertices = unsafe { slice::from_raw_parts(buffer[i..j].as_ptr() as *const [f64; 2], npoints) };
            vertices.chunks(4).map(|x| x[0]).collect::<Vec<_>>()
        };

        println!("{{ type: \"Feature\", properties: {{ id: \"{}\" }}, bbox: {:?}, geometry: {{ type: \"Polygon\", coordinates: [{:?}] }}}},", ids[idindex], bbox, vertices);

        offset += len;
        idindex += 1;
    }

    println!("]}};");
}
