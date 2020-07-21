#include <vector>
#include <cmath>
#include <iostream>
#include <fstream>

typedef std::vector<double> coordset;

struct object 
{
	//position, velocity, acceleration, and mass
	coordset r;
	coordset v;
	coordset a;
	double m;
};


double twoNorm(coordset cs)
{
	double res = 0;
	for (double d : cs)
	{
		res += d*d;
	}
	return sqrt(res);
}


//returns the vector pointing from s2 to s1
coordset diffVector(coordset s1, coordset s2)
{
	coordset difference;
	difference.resize(s1.size());
	for (size_t i = 0; i < difference.size(); i++)
	{
		difference[i] = s1[i] - s2[i];
	}
	return difference;
}

//euclidean distance of two vectors
double euclidDist(coordset s1, coordset s2)
{
	coordset difference = diffVector(s1, s2);
	return twoNorm(difference);
}

//rescales a vector to unit size
coordset makeUnit(coordset& cs)
{
	double mag = twoNorm(cs);
	for (double& d : cs)
	{
		d /= mag;
	}
	return cs;
}

//returns the acceleration vector of s2 due to the gravitatitonal interaction with object(s1,m1)
coordset gAcc(coordset s1, coordset s2, double m1) 
{
	coordset difference = diffVector(s1, s2);
	double mag = m1 / pow(twoNorm(difference),2);		//G is defined to be one
	makeUnit(difference);

	for (size_t i = 0; i < difference.size(); i++)
	{
		difference[i] *= mag;
	}

	return difference;
}

//return the total gravitational acceleration on the first object due to the other two
coordset totalAccVector(struct object o1, struct object o2, struct object o3)
{
	coordset part1;
	part1.resize(o1.r.size());
	part1 = gAcc(o2.r, o1.r, o2.m);

	coordset part2;
	part2.resize(o1.r.size());
	part2 = gAcc(o3.r, o1.r, o3.m);

	coordset res;
	res.resize(o1.r.size());
	res[0] = part1[0] + part2[0];
	res[1] = part1[1] + part2[1];

	return res;
}


void AMHW4()
{
	//initialize objects here
	struct object heavy;
	struct object sat;
	struct object dust;

	heavy.m = 100;
	heavy.r = { 0,0 };
	heavy.v = { 0,0 };
	heavy.a = { 0,0 };

	//use these two if the dynamics of the satellite are ignored (i.e. perfect circular motion)
	double omega_s = 0.3162277;
	double radsat = 10;

	//use these otherwise
	sat.m = 10;
	sat.r = { radsat,0 };
	sat.v = { 0,0 };
	sat.a = { 0,0 };

	dust.m = 0.001;
	dust.r = { 20,0 };
	dust.v = { 0,2.23606798 };	//circular obrit around the heavy object
	dust.a = totalAccVector(dust, sat, heavy);
	//end initialization


	std::fstream fstr;
	fstr.open("out.txt", std::ios::out | std::ios::trunc);
	double t; //time
	double angle;
	double delta = 0.001; //step size
	for (size_t i = 0; i < (10/delta); i++)
	{
		t = i * delta;
		fstr << t << " " << dust.r[0] << " " << dust.r[1] << " " << sat.r[0] << " " << sat.r[1] << " " << heavy.r[0] << " " << heavy.r[1] << "\n";

		dust.a = totalAccVector(dust, sat, heavy);
	
		dust.r[0] = dust.v[0] * delta + dust.r[0];
		dust.r[1] = dust.v[1] * delta + dust.r[1];

		dust.v[0] = dust.a[0] * delta + dust.v[0];
		dust.v[1] = dust.a[1] * delta + dust.v[1];

		//use this if the satellite's orbit is perfectly circular, comment otherwise
		angle = omega_s * t;
		sat.r[0] = radsat*cos(angle);
		sat.r[1] = radsat*sin(angle);
		
		//use these to apply the dynamics of gravity to the satellite and the heavy mass (3-body problem), comment otherwise
		/*
		sat.a = totalAccVector(sat, dust, heavy);
		sat.r[0] = sat.v[0] * delta + sat.r[0];
		sat.r[1] = sat.v[1] * delta + sat.r[1];
		sat.v[1] = sat.a[1] * delta + sat.v[1];
		sat.v[0] = sat.a[0] * delta + sat.v[0];

		heavy.a = totalAccVector(heavy, sat, dust);
		heavy.r[0] = heavy.v[0] * delta + heavy.r[0];
		heavy.r[1] = heavy.v[1] * delta + heavy.r[1];
		heavy.v[0] = heavy.a[0] * delta + heavy.v[0];
		heavy.v[1] = heavy.a[1] * delta + heavy.v[1];	
		*/
	}

	fstr.close();
}
