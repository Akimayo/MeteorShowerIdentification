using MeteorShowerIdentification.Rendering;
using MeteorShowerIdentification.Rendering.Astrodynamics;
using Microsoft.UI;

namespace MeteorShowerIdentification.Business;
internal static class StaticData
{
    public static CelestialBody Sun { get; } = new("Sun", Orbit.FromSemimajorAxis(0.0046525f, 0, 0, 0, 0), 10) { OrbitStroke = new SolidColorBrush(Colors.Goldenrod), OrbitStrokeThickness = 8 };
    public static IEnumerable<CelestialBody> Planets { get; } = new CelestialBody[] {
        new("Mercury", Orbit.FromSemimajorAxis(0.387098f, 0.205630f, 7.005f, 29.124f, 48.331f).WasDegrees(), 1) {OrbitStroke = new SolidColorBrush(Colors.SlateGray), OrbitStrokeThickness = 2 },
        new("Venus", Orbit.FromSemimajorAxis(0.723332f, 0.006772f, 3.39458f, 54.884f, 76.680f).WasDegrees(), 1) { OrbitStroke = new SolidColorBrush(Colors.LightYellow), OrbitStrokeThickness = 2 },
        new("Earth", Orbit.FromSemimajorAxis(1, 0.0167086f, 7.155f, 288.1f, 174.9f).WasDegrees(), 1) { OrbitStroke = new SolidColorBrush(Colors.Aqua), OrbitStrokeThickness = 2 },
        new("Mars", Orbit.FromSemimajorAxis(1.52368055f, 0.0934f, 1.850f, 286.5f, 49.57854f).WasDegrees(), 1) { OrbitStroke = new SolidColorBrush(Colors.OrangeRed), OrbitStrokeThickness = 2 },
        //new("Jupiter", Orbit.FromSemimajorAxis(5.2038f, 0.0489f, 1.303f, 273.867f, 100.464f).WasDegrees(), 3) { OrbitStroke = new SolidColorBrush(Colors.Orange) },
        //new("Saturn", Orbit.FromSemimajorAxis(9.5826f, 0.0565f, 2.485f, 339.392f, 113.665f).WasDegrees(), 3) { OrbitStroke = new SolidColorBrush(Colors.PaleGoldenrod) },
        //new("Uranus", Orbit.FromSemimajorAxis(19.19126f, 0.04717f, 0.773f, 96.998857f, 74.006f).WasDegrees(), 2) { OrbitStroke = new SolidColorBrush(Colors.SkyBlue) },
        //new("Neptune", Orbit.FromSemimajorAxis(30.07f, 0.008678f, 1.770f, 273.187f, 131.783f).WasDegrees(), 2) { OrbitStroke = new SolidColorBrush(Colors.LightSkyBlue) }
    };

    public static IEnumerable<CelestialBody> SimilarOrbits { get; } = new CelestialBody[] {
        new("Meteoroid 1", Orbit.FromPerihelionDistance(0.7457f, 0.95f, 30, 152.000f, 45).WasDegrees(), 0.1f),
        new("Meteoroid 2", Orbit.FromPerihelionDistance(0.9335f, 0.95f, 32, 153.694f, 42).WasDegrees(), 0.1f),
        new("Meteoroid 3", Orbit.FromPerihelionDistance(0.5954f, 0.95f, 32, 150.000f, 46).WasDegrees(), 0.1f),
        new("Meteoroid 4", Orbit.FromPerihelionDistance(0.5568f, 0.95f, 32, 149.339f, 46).WasDegrees(), 0.1f)
    };
    public static IEnumerable<CelestialBody> OrthogonalOrbits { get; } = new CelestialBody[] {
        new("Ortho X", Orbit.FromSemimajorAxis(20, 0, 0, 0, 0), 0) {OrbitStroke = new SolidColorBrush(Colors.Red), OrbitStrokeThickness = 1},
        new("Ortho Y", Orbit.FromSemimajorAxis(20, 0, (float)Math.PI/2, 0, 0), 0) { OrbitStroke = new SolidColorBrush(Colors.Green), OrbitStrokeThickness = 1 },
        new("Ortho Z", Orbit.FromSemimajorAxis(20, 0, 0, (float)Math.PI/2, 0), 0) { OrbitStroke = new SolidColorBrush(Colors.Blue), OrbitStrokeThickness = 1 }
    };
}
