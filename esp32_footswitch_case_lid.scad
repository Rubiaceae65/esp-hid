

difference() {
	union() {
		cube(size = [150, 100, 2]);
		difference() {
			cube(size = [150, 100, 16.0000000000]);
			translate(v = [2, 2, 0]) {
				cube(size = [146, 96, 16.0000000000]);
			}
		}
	}
	union() {
		translate(v = [-18.0000000000, 50.0000000000, 2]) {
			cylinder(d = 12, h = 22.1000000000);
		}
		translate(v = [13.0000000000, 50.0000000000, 2]) {
			cylinder(d = 12, h = 22.1000000000);
		}
		translate(v = [44.0000000000, 50.0000000000, 2]) {
			cylinder(d = 12, h = 22.1000000000);
		}
		translate(v = [75.0000000000, 50.0000000000, 2]) {
			cylinder(d = 12, h = 22.1000000000);
		}
		translate(v = [106.0000000000, 50.0000000000, 2]) {
			cylinder(d = 12, h = 22.1000000000);
		}
		translate(v = [137.0000000000, 50.0000000000, 2]) {
			cylinder(d = 12, h = 22.1000000000);
		}
		translate(v = [168.0000000000, 50.0000000000, 2]) {
			cylinder(d = 12, h = 22.1000000000);
		}
	}
	translate(v = [65.0000000000, 1.0000000000, 2]) {
		cylinder(center = true, d = 3, h = 2.1000000000);
	}
	union() {
		translate(v = [7, 7, 0]) {
			cylinder(d = 3.5000000000, h = 2.1000000000);
		}
		translate(v = [143, 7, 0]) {
			cylinder(d = 3.5000000000, h = 2.1000000000);
		}
		translate(v = [7, 93, 0]) {
			cylinder(d = 3.5000000000, h = 2.1000000000);
		}
		translate(v = [143, 93, 0]) {
			cylinder(d = 3.5000000000, h = 2.1000000000);
		}
	}
}