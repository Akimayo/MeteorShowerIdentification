using MeteorShowerIdentification.Rendering.Geometry;

namespace MeteorShowerIdentification.Rendering.Astrodynamics;
internal readonly struct Orbit
{
    public float SemiMajorAxis { get; }
    public float Eccentricity { get; }
    public float Inclination { get; }
    public float PerihelionArgument { get; }
    public float NodeLongitude { get; }

    /// <summary>
    /// Creates an <see cref="Orbit"/> from Kepler coordinates
    /// </summary>
    /// <param name="a">Semi-major axis</param>
    /// <param name="e">Eccentricity</param>
    /// <param name="i">Inclination</param>
    /// <param name="w">Argument of perihelion</param>
    /// <param name="O">Longitude of ascending node</param>
    private Orbit(float a, float e, float i, float w, float O)
    {
        SemiMajorAxis = a;
        Eccentricity = e;
        Inclination = i;
        PerihelionArgument = w;
        NodeLongitude = O;
    }
    /// <summary>
    /// Creates an <see cref="Orbit"/> from Kepler coordinates using perihelion distance <paramref name="q"/>.
    /// </summary>
    /// <param name="q">Perihelion distance</param>
    /// <param name="e">Eccentricity</param>
    /// <param name="i">Inclination</param>
    /// <param name="w">Argument of perihelion</param>
    /// <param name="O">Longitude of ascending node</param>
    /// <returns>The heliocentric orbit</returns>
    public static Orbit FromPerihelionDistance(float q, float e, float i, float w, float O) =>
        new(q / (1 - e), e, i, w, O);
    /// <summary>
    /// Creates an <see cref="Orbit"/> from Kepler coordinates using semi-major axis <paramref name="a"/>.
    /// </summary>
    /// <param name="a">Semi-major axis</param>
    /// <param name="e">Eccentricity</param>
    /// <param name="i">Inclination</param>
    /// <param name="w">Argument of perihelion</param>
    /// <param name="O">Longitude of ascending node</param>
    /// <returns></returns>
    public static Orbit FromSemimajorAxis(float a, float e, float i, float w, float O) =>
        new(a, e, i, w, O);
    /// <summary>
    /// Converts angles to radians
    /// </summary>
    /// <returns>A new <see cref="Orbit"/> with angles in radians</returns>
    public Orbit WasDegrees() => new(SemiMajorAxis, Eccentricity, (float)(Inclination / 180 * Math.PI), (float)(PerihelionArgument / 180 * Math.PI), (float)(NodeLongitude / 180 * Math.PI));

    public Ellipse AsEllipse() =>
        (new Ellipse(
            new(SemiMajorAxis * Eccentricity, 0), // Focus of the ellipse is located at origin
            SemiMajorAxis,
            (float)Math.Sqrt(SemiMajorAxis * SemiMajorAxis * (1 - Eccentricity * Eccentricity))) // Calculate semi-minor axis
        ).Rotate(new(PerihelionArgument, Inclination, NodeLongitude));
}
