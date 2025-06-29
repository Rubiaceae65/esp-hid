

union() {
	union() {
		difference() {
			union() {
				cube(size = [150, 100, 2]);
				difference() {
					cube(size = [150, 100, 30]);
					translate(v = [2, 2, 2]) {
						cube(size = [146, 96, 28]);
					}
				}
			}
			translate(v = [75.0000000000, 0, 13.5000000000]) {
				cube(center = true, size = [10, 2.1000000000, 5]);
			}
		}
		difference() {
			union() {
				translate(v = [62.8500000000, 42.3000000000, 2]) {
					cylinder(d = 4, h = 5);
				}
				translate(v = [87.1500000000, 42.3000000000, 2]) {
					cylinder(d = 4, h = 5);
				}
				translate(v = [62.8500000000, 57.7000000000, 2]) {
					cylinder(d = 4, h = 5);
				}
				translate(v = [87.1500000000, 57.7000000000, 2]) {
					cylinder(d = 4, h = 5);
				}
			}
			union() {
				translate(v = [62.8500000000, 42.3000000000, 2]) {
					cylinder(d = 2.5000000000, h = 5.1000000000);
				}
				translate(v = [87.1500000000, 42.3000000000, 2]) {
					cylinder(d = 2.5000000000, h = 5.1000000000);
				}
				translate(v = [62.8500000000, 57.7000000000, 2]) {
					cylinder(d = 2.5000000000, h = 5.1000000000);
				}
				translate(v = [87.1500000000, 57.7000000000, 2]) {
					cylinder(d = 2.5000000000, h = 5.1000000000);
				}
			}
		}
	}
	translate(v = [0, 0, 28]) {
		difference() {
			cube(size = [150, 100, 2]);
			union() {
				translate(v = [-18.0000000000, 50.0000000000, 0]) {
					cylinder(d = 12, h = 2.1000000000);
				}
				translate(v = [13.0000000000, 50.0000000000, 0]) {
					cylinder(d = 12, h = 2.1000000000);
				}
				translate(v = [44.0000000000, 50.0000000000, 0]) {
					cylinder(d = 12, h = 2.1000000000);
				}
				translate(v = [75.0000000000, 50.0000000000, 0]) {
					cylinder(d = 12, h = 2.1000000000);
				}
				translate(v = [106.0000000000, 50.0000000000, 0]) {
					cylinder(d = 12, h = 2.1000000000);
				}
				translate(v = [137.0000000000, 50.0000000000, 0]) {
					cylinder(d = 12, h = 2.1000000000);
				}
				translate(v = [168.0000000000, 50.0000000000, 0]) {
					cylinder(d = 12, h = 2.1000000000);
				}
			}
			translate(v = [65.0000000000, 1.0000000000, 29.0000000000]) {
				cylinder(center = true, d = 3, h = 2.1000000000);
			}
		}
	}
}