namespace MeteorShowerIdentification.Rendering.Geometry;
/// <summary>
/// An approximation of an ellipse with Beziér curves.
/// </summary>
/// <remarks>
/// Source: <see href="https://stackoverflow.com/a/20582153"/>
/// </remarks>
internal readonly struct Ellipse
{
    private readonly Bezier[] _curves = new Bezier[2];

    public Vector StartPoint { get; }
    public readonly Bezier Segment1 => _curves[0];
    public readonly Bezier Segment2 => _curves[1];
    public static Ellipse operator +(Ellipse a, Vector b) => new(a.StartPoint + b, a.Segment1 + b, a.Segment2 + b);
    public static Ellipse operator *(Ellipse a, float n) => new(a.StartPoint * n, a.Segment1 * n, a.Segment2 * n);

#if DEBUG
    private readonly float _major, _minor;
#endif

    public Ellipse(Vector center, float major, float minor)
    {
        StartPoint = new(center.X, center.Y - minor, center.Z);
        float cpX = major * 4 / 3;
        _curves[0] = new(new(center.X + cpX, center.Y - minor, center.Z),
                         new(center.X + cpX, center.Y + minor, center.Z),
                         new(center.X, center.Y + minor, center.Z));
        _curves[1] = new(new(center.X - cpX, center.Y + minor, center.Z),
                         new(center.X - cpX, center.Y - minor, center.Z),
                         StartPoint);
#if DEBUG
        _major = major;
        _minor = minor;
#endif
    }
    public Ellipse(Vector startPoint, Bezier segment1, Bezier segment2)
    {
        StartPoint = startPoint;
        _curves[0] = segment1;
        _curves[1] = segment2;
    }

#if DEBUG
    public override string ToString() => $"Ellipse a={_major}, b={_minor}";
#endif
}
