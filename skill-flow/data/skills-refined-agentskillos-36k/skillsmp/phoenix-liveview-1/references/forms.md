# LiveView Forms Reference

## File Uploads

### Basic Upload

```elixir
defmodule MyAppWeb.UploadLive do
  use MyAppWeb, :live_view

  def mount(_params, _session, socket) do
    {:ok,
     socket
     |> assign(:uploaded_files, [])
     |> allow_upload(:avatar,
       accept: ~w(.jpg .jpeg .png),
       max_entries: 1,
       max_file_size: 5_000_000
     )}
  end

  def handle_event("validate", _params, socket) do
    {:noreply, socket}
  end

  def handle_event("save", _params, socket) do
    uploaded_files =
      consume_uploaded_entries(socket, :avatar, fn %{path: path}, entry ->
        dest = Path.join(["priv", "static", "uploads", "#{entry.uuid}.#{ext(entry)}"])
        File.cp!(path, dest)
        {:ok, ~p"/uploads/#{Path.basename(dest)}"}
      end)

    {:noreply,
     socket
     |> update(:uploaded_files, &(&1 ++ uploaded_files))
     |> put_flash(:info, "File uploaded successfully")}
  end

  def handle_event("cancel", %{"ref" => ref}, socket) do
    {:noreply, cancel_upload(socket, :avatar, ref)}
  end

  defp ext(entry) do
    [ext | _] = MIME.extensions(entry.client_type)
    ext
  end
end
```

### Template

```heex
<.simple_form for={%{}} phx-change="validate" phx-submit="save">
  <.live_file_input upload={@uploads.avatar} />

  <%= for entry <- @uploads.avatar.entries do %>
    <div class="upload-entry">
      <.live_img_preview entry={entry} width="75" />
      <span><%= entry.client_name %></span>
      <button type="button" phx-click="cancel" phx-value-ref={entry.ref}>
        Cancel
      </button>

      <%= for err <- upload_errors(@uploads.avatar, entry) do %>
        <p class="error"><%= error_to_string(err) %></p>
      <% end %>
    </div>
  <% end %>

  <:actions>
    <.button>Upload</.button>
  </:actions>
</.simple_form>
```

### Upload to S3

```elixir
def mount(_params, _session, socket) do
  {:ok,
   socket
   |> allow_upload(:photos,
     accept: ~w(.jpg .jpeg .png),
     max_entries: 5,
     external: &presign_upload/2
   )}
end

defp presign_upload(entry, socket) do
  {:ok, presigned_url} =
    S3.presign_put(
      "my-bucket",
      "uploads/#{entry.uuid}",
      expires_in: 3600
    )

  meta = %{
    uploader: "S3",
    key: "uploads/#{entry.uuid}",
    url: presigned_url
  }

  {:ok, meta, socket}
end

def handle_event("save", _params, socket) do
  uploaded_files =
    consume_uploaded_entries(socket, :photos, fn _meta, entry ->
      # File already uploaded to S3 via presigned URL
      {:ok, "uploads/#{entry.uuid}"}
    end)

  {:noreply, assign(socket, :uploaded_files, uploaded_files)}
end
```

## Nested Forms

### Embedded Schema

```elixir
defmodule MyApp.Order do
  use Ecto.Schema
  import Ecto.Changeset

  embedded_schema do
    field :customer_name, :string
    embeds_many :line_items, LineItem
  end

  def changeset(order, attrs) do
    order
    |> cast(attrs, [:customer_name])
    |> cast_embed(:line_items, required: true)
    |> validate_required([:customer_name])
  end
end

defmodule MyApp.LineItem do
  use Ecto.Schema
  import Ecto.Changeset

  embedded_schema do
    field :product_name, :string
    field :quantity, :integer
  end

  def changeset(line_item, attrs) do
    line_item
    |> cast(attrs, [:product_name, :quantity])
    |> validate_required([:product_name, :quantity])
    |> validate_number(:quantity, greater_than: 0)
  end
end
```

### LiveView

```elixir
def mount(_params, _session, socket) do
  changeset = Order.changeset(%Order{line_items: [%LineItem{}]}, %{})

  {:ok, assign(socket, :form, to_form(changeset))}
end

def handle_event("add_line_item", _, socket) do
  existing = Ecto.Changeset.get_field(socket.assigns.form.source, :line_items)
  changeset =
    socket.assigns.form.source
    |> Ecto.Changeset.put_embed(:line_items, existing ++ [%LineItem{}])

  {:noreply, assign(socket, :form, to_form(changeset))}
end

def handle_event("remove_line_item", %{"index" => index}, socket) do
  index = String.to_integer(index)
  existing = Ecto.Changeset.get_field(socket.assigns.form.source, :line_items)

  changeset =
    socket.assigns.form.source
    |> Ecto.Changeset.put_embed(:line_items, List.delete_at(existing, index))

  {:noreply, assign(socket, :form, to_form(changeset))}
end
```

### Template

```heex
<.simple_form for={@form} phx-change="validate" phx-submit="save">
  <.input field={@form[:customer_name]} label="Customer Name" />

  <h3>Line Items</h3>
  <.inputs_for :let={item_form} field={@form[:line_items]}>
    <.input field={item_form[:product_name]} label="Product" />
    <.input field={item_form[:quantity]} type="number" label="Quantity" />
    <button type="button" phx-click="remove_line_item" phx-value-index={item_form.index}>
      Remove
    </button>
  </.inputs_for>

  <button type="button" phx-click="add_line_item">Add Line Item</button>

  <:actions>
    <.button>Submit</.button>
  </:actions>
</.simple_form>
```

## Dynamic Inputs

### Conditional Fields

```elixir
def handle_event("validate", %{"user" => user_params}, socket) do
  changeset =
    %User{}
    |> User.changeset(user_params)
    |> Map.put(:action, :validate)

  {:noreply, assign(socket, :form, to_form(changeset))}
end
```

```heex
<.simple_form for={@form} phx-change="validate" phx-submit="save">
  <.input field={@form[:account_type]} type="select" options={["personal", "business"]} />

  <div :if={@form.params["account_type"] == "business"}>
    <.input field={@form[:company_name]} label="Company Name" />
    <.input field={@form[:tax_id]} label="Tax ID" />
  </div>

  <div :if={@form.params["account_type"] == "personal"}>
    <.input field={@form[:date_of_birth]} type="date" label="Date of Birth" />
  </div>

  <:actions>
    <.button>Save</.button>
  </:actions>
</.simple_form>
```

### Multi-Step Forms

```elixir
def mount(_params, _session, socket) do
  {:ok,
   socket
   |> assign(:step, 1)
   |> assign(:form_data, %{})
   |> assign_form(%{})}
end

def handle_event("next", %{"user" => params}, socket) do
  case socket.assigns.step do
    1 ->
      # Validate step 1
      changeset = User.step1_changeset(%User{}, params)

      if changeset.valid? do
        {:noreply,
         socket
         |> assign(:step, 2)
         |> update(:form_data, &Map.merge(&1, params))
         |> assign_form(%{})}
      else
        {:noreply, assign(socket, :form, to_form(changeset))}
      end

    2 ->
      # Validate step 2 and save
      all_params = Map.merge(socket.assigns.form_data, params)
      changeset = User.changeset(%User{}, all_params)

      case Repo.insert(changeset) do
        {:ok, user} ->
          {:noreply,
           socket
           |> put_flash(:info, "Account created!")
           |> push_navigate(to: ~p"/users/#{user}")}

        {:error, changeset} ->
          {:noreply, assign(socket, :form, to_form(changeset))}
      end
  end
end

def handle_event("back", _, socket) do
  {:noreply, update(socket, :step, &(&1 - 1))}
end

defp assign_form(socket, params) do
  changeset =
    case socket.assigns.step do
      1 -> User.step1_changeset(%User{}, params)
      2 -> User.step2_changeset(%User{}, params)
    end
    |> Map.put(:action, :validate)

  assign(socket, :form, to_form(changeset))
end
```

## Form Validation Patterns

### Real-Time Validation

```elixir
def handle_event("validate_email", %{"email" => email}, socket) do
  Task.start(fn ->
    available = Accounts.email_available?(email)
    send(self(), {:email_check_result, email, available})
  end)

  {:noreply, assign(socket, :checking_email, true)}
end

def handle_info({:email_check_result, email, available}, socket) do
  if socket.assigns.form.params["email"] == email do
    changeset =
      socket.assigns.form.source
      |> then(fn changeset ->
        if available do
          changeset
        else
          Ecto.Changeset.add_error(changeset, :email, "is already taken")
        end
      end)

    {:noreply,
     socket
     |> assign(:checking_email, false)
     |> assign(:form, to_form(changeset))}
  else
    {:noreply, assign(socket, :checking_email, false)}
  end
end
```

### Custom Validation

```elixir
def changeset(user, attrs) do
  user
  |> cast(attrs, [:password, :password_confirmation])
  |> validate_required([:password])
  |> validate_length(:password, min: 12)
  |> validate_password_strength()
  |> validate_confirmation(:password, message: "does not match password")
end

defp validate_password_strength(changeset) do
  password = get_field(changeset, :password)

  cond do
    is_nil(password) ->
      changeset

    String.match?(password, ~r/[A-Z]/) and
    String.match?(password, ~r/[a-z]/) and
    String.match?(password, ~r/[0-9]/) ->
      changeset

    true ->
      add_error(changeset, :password, "must contain uppercase, lowercase, and numbers")
  end
end
```

## Error Display

### Field-Level Errors

```heex
<.input field={@form[:email]} label="Email" required />
<!-- CoreComponents.input automatically shows field errors -->
```

### Form-Level Errors

```elixir
def handle_event("save", params, socket) do
  case Accounts.create_user(params) do
    {:ok, user} ->
      {:noreply,
       socket
       |> put_flash(:info, "User created")
       |> push_navigate(to: ~p"/users/#{user}")}

    {:error, %Ecto.Changeset{} = changeset} ->
      {:noreply,
       socket
       |> assign(:form, to_form(changeset))
       |> put_flash(:error, "Please fix the errors below")}
  end
end
```

### Custom Error Component

```heex
<.error :if={@form.errors != []}>
  <%= for {field, {msg, _}} <- @form.errors do %>
    <li><%= Phoenix.Naming.humanize(field) %>: <%= msg %></li>
  <% end %>
</.error>
```

## Form Security

### CSRF Protection

CSRF tokens are automatically included via `<.simple_form>`. If building custom forms:

```heex
<form phx-submit="save">
  <input type="hidden" name="_csrf_token" value={get_csrf_token()} />
  <!-- form fields -->
</form>
```

### Rate Limiting

```elixir
def handle_event("save", params, socket) do
  case RateLimiter.check_rate(socket.assigns.current_user, :create_post) do
    {:ok, _} ->
      # Process form
      create_post(params)

    {:error, _} ->
      {:noreply,
       socket
       |> put_flash(:error, "Too many requests. Please try again later.")
       |> assign(:form, to_form(changeset))}
  end
end
```
