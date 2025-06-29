

union() {
	difference() {
		union() {
			cube(size = [150, 100, 2]);
			difference() {
				cube(size = [150, 100, 14.0000000000]);
				translate(v = [2, 2, 0]) {
					cube(size = [146, 96, 14.0000000000]);
				}
			}
		}
		translate(v = [75.0000000000, 0, 6.5000000000]) {
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
	difference() {
		union() {
			translate(v = [7, 7, 2]) {
				cylinder(d = 6, h = 5);
			}
			translate(v = [143, 7, 2]) {
				cylinder(d = 6, h = 5);
			}
			translate(v = [7, 93, 2]) {
				cylinder(d = 6, h = 5);
			}
			translate(v = [143, 93, 2]) {
				cylinder(d = 6, h = 5);
			}
		}
		union() {
			translate(v = [7, 7, 2]) {
				cylinder(d = 3, h = 10);
			}
			translate(v = [143, 7, 2]) {
				cylinder(d = 3, h = 10);
			}
			translate(v = [7, 93, 2]) {
				cylinder(d = 3, h = 10);
			}
			translate(v = [143, 93, 2]) {
				cylinder(d = 3, h = 10);
			}
		}
	}
}