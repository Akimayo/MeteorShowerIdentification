namespace MeteorShowerIdentification.Presentation;

public partial class MainViewModel : ObservableObject
{
    private INavigator _navigator;

    [ObservableProperty]
    private string? name;

    public MainViewModel(
        IStringLocalizer localizer,
        IOptions<AppConfig> appInfo,
        INavigator navigator)
    {
        _navigator = navigator;
        Title = "Main";
        Title += $" - {localizer["ApplicationName"]}";
        Title += $" - {appInfo?.Value?.Environment}";
        GoToSecond = new AsyncRelayCommand(GoToSecondView);
        GoToRenderer = new AsyncRelayCommand(GoToRendererView);
    }
    public string? Title { get; }

    public ICommand GoToSecond { get; }
    public ICommand GoToRenderer { get; }

    private async Task GoToSecondView()
    {
        await _navigator.NavigateViewModelAsync<SecondViewModel>(this, data: new Entity(Name!));
    }
    private async Task GoToRendererView()
    {
        await _navigator.NavigateViewAsync<RendererPage>(this);
    }

}
